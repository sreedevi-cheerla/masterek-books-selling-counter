from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.inventory import Book
from app.schemas.inventory import BookCreate, BookResponse
from app.services.excel_service import ExcelService

router = APIRouter(prefix="/admin", tags=["Administration"])

@router.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def add_book(payload: BookCreate, db: Session = Depends(get_db)):
    existing_book = db.query(Book).filter(Book.name == payload.name.strip()).first()
    if existing_book:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A book with this name already exists."
        )

    book = Book(
        name=payload.name.strip(),
        language=payload.language.strip(),
        category=payload.category.strip(),
        original_price=payload.original_price,
        discount_percentage=payload.discount_percentage,
        available_copies=payload.available_copies
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

@router.post("/import-inventory")
async def import_inventory(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid document format. Please upload a valid Excel workbook file."
        )
    try:
        contents = await file.read()
        ExcelService.import_inventory(contents, db)
        return {"status": "success", "message": "Master book list imported successfully into the inventory."}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

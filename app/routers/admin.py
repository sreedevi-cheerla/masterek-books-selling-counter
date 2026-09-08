from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.excel_service import ExcelService

router = APIRouter(prefix="/admin", tags=["Administration"])

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

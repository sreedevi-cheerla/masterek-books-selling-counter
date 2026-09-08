from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.excel_service import ExcelService

router = APIRouter(prefix="/reports", tags=["Reporting Engines"])

@router.get("/export", response_class=StreamingResponse)
def export_sales_and_stock_reports(db: Session = Depends(get_db)):
    excel_stream = ExcelService.generate_reports(db)
    
    return StreamingResponse(
        excel_stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=Guru_Pooja_Sales_Stock_Report.xlsx"}
    )

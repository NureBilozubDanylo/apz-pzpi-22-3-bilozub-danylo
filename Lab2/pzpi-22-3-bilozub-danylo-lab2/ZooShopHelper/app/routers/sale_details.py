from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.sale_details import SaleDetailsCreate, SaleDetails
from app.crud.sale_details import create_sale_detail, get_sale_details_by_sale_id
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=SaleDetails)
def create_sale_detail_endpoint(sale_detail: SaleDetailsCreate, db: Session = Depends(get_db)):
    return create_sale_detail(db, sale_detail)

@router.get("/{sale_id}", response_model=list[SaleDetails])
def get_sale_details(sale_id: int, db: Session = Depends(get_db)):
    sale_details = get_sale_details_by_sale_id(db, sale_id)
    if not sale_details:
        raise HTTPException(status_code=404, detail="Sale details not found")
    return sale_details

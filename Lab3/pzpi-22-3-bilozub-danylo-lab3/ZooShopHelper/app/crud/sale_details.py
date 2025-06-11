from sqlalchemy.orm import Session
from app.models.sale_details import SaleDetails
from app.schemas.sale_details import SaleDetailsCreate

def create_sale_detail(db: Session, sale_detail: SaleDetailsCreate):
    db_sale_detail = SaleDetails(
        sale_id=sale_detail.sale_id,
        shop_supplies_id=sale_detail.shop_supplies_id,
        quantity=sale_detail.quantity,
        total_price=sale_detail.total_price
    )
    db.add(db_sale_detail)
    db.commit()
    db.refresh(db_sale_detail)
    return db_sale_detail

def get_sale_details_by_sale_id(db: Session, sale_id: int):
    return db.query(SaleDetails).filter(SaleDetails.sale_id == sale_id).all()

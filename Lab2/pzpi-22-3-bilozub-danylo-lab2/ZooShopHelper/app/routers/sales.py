from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.crud import sales as crud_sales
from app.schemas.sales import Sales, SalesCreate, SaleConfirmation
from app.dependencies import get_current_user, get_current_admin_user
from app.crud.sale_details import get_sale_details_by_sale_id
from datetime import date
from app.crud.supplies import get_supply_name_by_id  # Import the new function

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Sales)
def create_sale(sale: SalesCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return crud_sales.create_sale(db=db, sale=sale)

@router.get("/user/{user_id}", response_model=List[Sales])
def get_sales_by_user_id(user_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    sales = crud_sales.get_sales_by_user_id(db, user_id=user_id)
    if not sales:
        raise HTTPException(status_code=404, detail="No sales found for this user")
    return sales

@router.get("/shop/{shop_id}")
def get_sales_by_shop_id(shop_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    today = date.today()
    sales = crud_sales.get_sales_by_shop_id_and_date(db, shop_id=shop_id, sale_date=today)
    if not sales:
        raise HTTPException(status_code=404, detail="No sales found for this shop today")
    
    receipts = []
    for sale in sales:
        sale_details = get_sale_details_by_sale_id(db, sale_id=sale.sale_id)
        items = [
            {
                "product_id": detail.shop_supplies_id,
                "name": crud_sales.get_supply_name_by_shop_supplies_id(db, detail.shop_supplies_id),  # Fetch the product name
                "quantity": detail.quantity,
                "price": detail.total_price / detail.quantity,
                "total": detail.total_price,
            }
            for detail in sale_details
        ]
        receipts.append({
            "id": sale.sale_id,
            "items": items,
            "total": sum(item["total"] for item in items),
        })

    return receipts

@router.post("/confirm")
def confirm_sale(sale_data: SaleConfirmation, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # Create a single sale instance
    sale = crud_sales.create_sale_instance(
        db=db,
        user_id=current_user.user_id,
        shop_id=sale_data.shop_id,
        pay_type=sale_data.paymentType
    )
    
    # Associate products with the sale
    for product in sale_data.products:
        shop_supplies_id = crud_sales.get_shop_supplies_id(
            db=db,
            shop_id=sale_data.shop_id,
            supply_id=product.supply_id
        )
        crud_sales.add_product_to_sale(
            db=db,
            sale_id=sale.sale_id,
            shop_supplies_id=shop_supplies_id,
            quantity=product.count,
            total_price=product.sale_price * product.count
        )
        
        # Deduct the sold quantity from shop_supplies
        crud_sales.update_shop_supplies_quantity(
            db=db,
            shop_supplies_id=shop_supplies_id,
            quantity_to_deduct=product.count
        )
    
    return {"message": "Sale confirmed", "sale_id": sale.sale_id}

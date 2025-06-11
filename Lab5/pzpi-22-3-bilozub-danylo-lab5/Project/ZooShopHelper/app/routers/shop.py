from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import shop as crud_shop
from app.models.user import User
from app.models.employee import Employee
from app.schemas.shop import Shop1, ShopBase, ShopCreate, ShopUpdate
from app.dependencies import get_current_user, get_current_admin_user
from typing import List
from app.crud import sales as crud_sales
from datetime import date
from app.crud.sale_details import get_sale_details_by_sale_id
from app.crud.request import create_request
from app.schemas.request import RequestCreate, RequestResponse
from app.models.shop import Shop

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Shop1)
def create_shop(shop: ShopCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    return crud_shop.create_shop(db=db, shop=shop)

@router.get("/{shop_id}", response_model=Shop1)
def read_shop(shop_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_shop = crud_shop.get_shop(db, shop_id=shop_id)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop

@router.put("/{shop_id}", response_model=Shop1)
def update_shop(shop_id: int, shop: ShopUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_shop = crud_shop.update_shop(db, shop_id=shop_id, shop=shop)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop

@router.delete("/{shop_id}", response_model=Shop1)
def delete_shop(shop_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_shop = crud_shop.delete_shop(db, shop_id=shop_id)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop

@router.get("/user/{username}/shops", response_model=List[Shop1])
def get_shops_by_username(username: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    shops = crud_shop.get_shops_by_username(db, username=username)
    if not shops:
        raise HTTPException(status_code=404, detail="No shops found for this user")
    return shops

@router.get("/{shop_id}/stats")
def get_shop_stats(shop_id: int, sales_date: date = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not sales_date:
        raise HTTPException(status_code=400, detail="Sales date must be provided as a query parameter")
    
    sales = crud_sales.get_sales_by_shop_and_date(db, shop_id=shop_id, sales_date=sales_date)
    if not sales:
        raise HTTPException(status_code=404, detail="No sales found for this shop on the given date")
    
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
                "purchase_price": crud_sales.get_supply_purchase_price_by_shop_supplies_id(db, detail.shop_supplies_id),  # Fetch the purchase price
            }
            for detail in sale_details
        ]
        receipts.append({
            "id": sale.sale_id,
            "items": items,
            "total": sum(item["total"] for item in items),
        })

    return receipts

@router.get("/{shop_id}/workers", response_model=List[dict])
def get_shop_workers(shop_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Fetch all users (workers) associated with a specific shop by shop_id, including the shop owner.
    """
    # Fetch employees associated with the shop
    employees = db.query(Employee).filter(Employee.shop_id == shop_id).all()


    # Combine employee and user information
    workers = []
    for employee in employees:
        user = db.query(User).filter(User.user_id == employee.user_id).first()
        if user:
            workers.append({
                "shop_id": employee.shop_id,
                "user_id": employee.user_id,
                "role": user.role,
                "username": user.username,
                "email": user.email,
                "mobile_number": user.mobile_number,
                "age": user.age,
                "position": employee.position,
                "salary_without_percent": employee.salary_without_percent,
            })

    # Fetch the shop owner
    shop_owner_id = db.query(Shop).filter(Shop.shop_id == shop_id).first().user_id
    owner_user = db.query(User).filter(User.user_id == shop_owner_id).first()
    if owner_user:
        workers.append({
            "shop_id": shop_id,
            "user_id": owner_user.user_id,
            "role": owner_user.role,
            "username": owner_user.username,
            "email": owner_user.email,
            "mobile_number": owner_user.mobile_number,
            "age": owner_user.age,
            "position": "Owner",
            "salary_without_percent": None, 
        })

    return workers

@router.delete("/workers/{worker_id}")
def dismiss_worker(worker_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    """
    Dismiss a worker by setting their shop_id to null.
    """
    employee = db.query(Employee).filter(Employee.user_id == worker_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Worker not found in this shop")
    
    # Set shop_id to null
    employee.shop_id = None
    db.commit()
    db.refresh(employee)
    
    return {"message": "Worker dismissed successfully", "worker_id": worker_id}

@router.get("/{shop_id}/another-workers")
def get_another_workers(shop_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Fetch all users who are not associated with a specific shop by shop_id.
    """
    # Fetch all employees associated with the shop
    associated_users = db.query(Employee.user_id).filter(Employee.shop_id == shop_id).subquery()

    # Fetch users not associated with the shop
    users = db.query(User).filter(~User.user_id.in_(associated_users)).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found who are not associated with this shop")

    # Combine user information
    another_workers = [
        {
            "user_id": user.user_id,
            "role": user.role,
            "username": user.username,
            "email": user.email,
            "mobile_number": user.mobile_number,
            "age": user.age,
        }
        for user in users
    ]

    return another_workers

@router.post("/{shop_id}/invite", response_model=RequestResponse)
def send_invitation(shop_id: int, request_data: RequestCreate, db: Session = Depends(get_db)):
    if shop_id != request_data.shop_id:
        raise HTTPException(status_code=400, detail="Shop ID mismatch")
    return create_request(db, request_data)

from sqlalchemy.orm import Session
from app.models.shop import Shop
from app.models.user import User
from app.models.employee import Employee
from app.schemas.shop import ShopCreate, ShopUpdate

def create_shop(db: Session, shop: ShopCreate):
    db_shop = Shop(**shop.dict())
    db.add(db_shop)
    db.commit()
    db.refresh(db_shop)
    return db_shop

def get_shop(db: Session, shop_id: int):
    return db.query(Shop).filter(Shop.shop_id == shop_id).first()

def update_shop(db: Session, shop_id: int, shop: ShopUpdate):
    db_shop = db.query(Shop).filter(Shop.shop_id == shop_id).first()
    if db_shop:
        for key, value in shop.dict().items():
            setattr(db_shop, key, value)
        db.commit()
        db.refresh(db_shop)
    return db_shop

def delete_shop(db: Session, shop_id: int):
    db_shop = db.query(Shop).filter(Shop.shop_id == shop_id).first()
    if db_shop:
        db.delete(db_shop)
        db.commit()
    return db_shop

def get_shops_by_user_id(db: Session, user_id: int):
    return db.query(Shop).filter(Shop.user_id == user_id).all()

def get_shops_by_username(db: Session, username: str):
    """
    Fetch all shops owned by the user or where the user works as an employee.
    """
    # Find the user by username
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return []

    # Get shops owned by the user
    owned_shops = db.query(Shop).filter(Shop.user_id == user.user_id).all()

    # Get shops where the user works as an employee
    employee_shop_ids = db.query(Employee.shop_id).filter(Employee.user_id == user.user_id).all()
    employee_shop_ids = [shop_id for shop_id, in employee_shop_ids]  # Unpack tuples
    employee_shops = db.query(Shop).filter(Shop.shop_id.in_(employee_shop_ids)).all()

    # Combine and return unique shops
    return list({shop.shop_id: shop for shop in owned_shops + employee_shops}.values())

def get_workers_by_shop_id(db: Session, shop_id: int):
    """
    Fetch all workers associated with a specific shop by shop_id, including user details.
    """
    return db.query(Employee).filter(Employee.shop_id == shop_id).all()

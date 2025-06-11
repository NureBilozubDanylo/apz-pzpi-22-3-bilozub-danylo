from datetime import date
from sqlalchemy.orm import Session
from app.models.sales import Sales
from app.schemas.sales import SalesCreate
from app.models.sale_details import SaleDetails
from app.models.shop_supplies import ShopSupplies
from app.models.supplies import Supplies

def create_sale(db: Session, sale: SalesCreate):
    db_sale = Sales(**sale.dict())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

def get_sales_by_user_id(db: Session, user_id: int):
    return db.query(Sales).filter(Sales.user_id == user_id).all()

def create_sale_instance(db: Session, user_id: int, shop_id: int, pay_type: str):
    sale = Sales(user_id=user_id, shop_id=shop_id, sale_date=date.today(), pay_type=pay_type)
    db.add(sale)
    db.commit()
    db.refresh(sale)
    return sale

def add_product_to_sale(db: Session, sale_id: int, shop_supplies_id: int, quantity: int, total_price: float):
    sale_detail = SaleDetails(
        sale_id=sale_id,
        shop_supplies_id=shop_supplies_id,
        quantity=quantity,
        total_price=total_price
    )
    db.add(sale_detail)
    db.commit()
    return sale_detail

def get_shop_supplies_id(db: Session, shop_id: int, supply_id: int):
    shop_supply = db.query(ShopSupplies).filter(
        ShopSupplies.shop_id == shop_id,
        ShopSupplies.supply_id == supply_id
    ).first()
    if not shop_supply:
        raise ValueError(f"No shop_supplies entry found for shop_id={shop_id} and supply_id={supply_id}")
    return shop_supply.shop_supplies_id

def get_sales_by_shop_id(db: Session, shop_id: int):
    return db.query(Sales).filter(Sales.shop_id == shop_id).all()

def get_sales_by_shop_id_and_date(db: Session, shop_id: int, sale_date: date):
    return db.query(Sales).filter(Sales.shop_id == shop_id, Sales.sale_date == sale_date).all()

def get_supply_name_by_shop_supplies_id(db: Session, shop_supplies_id: int) -> str:
    shop_supply = db.query(ShopSupplies).filter(ShopSupplies.shop_supplies_id == shop_supplies_id).first()
    if not shop_supply:
        raise ValueError(f"No shop_supplies entry found for shop_supplies_id={shop_supplies_id}")
    
    supply = db.query(Supplies).filter(Supplies.supply_id == shop_supply.supply_id).first()
    if not supply:
        raise ValueError(f"No supply found for supply_id={shop_supply.supply_id}")
    
    return supply.name

def update_shop_supplies_quantity(db: Session, shop_supplies_id: int, quantity_to_deduct: int):
    shop_supply = db.query(ShopSupplies).filter(ShopSupplies.shop_supplies_id == shop_supplies_id).first()
    if not shop_supply:
        raise ValueError("Shop supply not found")
    if shop_supply.quantity < quantity_to_deduct:
        raise ValueError("Insufficient stock in shop supplies")
    shop_supply.quantity -= quantity_to_deduct
    db.commit()
    db.refresh(shop_supply)
    return shop_supply

def get_sales_by_shop_and_date(db: Session, shop_id: int, sales_date: date):
    return db.query(Sales).filter(
        Sales.shop_id == shop_id,
        Sales.sale_date == sales_date
    ).all()

def get_supply_purchase_price_by_shop_supplies_id(db: Session, shop_supplies_id: int) -> float:
    shop_supply = db.query(ShopSupplies).filter(ShopSupplies.shop_supplies_id == shop_supplies_id).first()
    if not shop_supply:
        raise ValueError(f"No shop_supplies entry found for shop_supplies_id={shop_supplies_id}")
    
    supply = db.query(Supplies).filter(Supplies.supply_id == shop_supply.supply_id).first()
    if not supply:
        raise ValueError(f"No supply found for supply_id={shop_supply.supply_id}")
    
    return supply.purchase_price
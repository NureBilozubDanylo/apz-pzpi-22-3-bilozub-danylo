from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import supplies as crud_supplies
from app.crud import shop_supplies as crud_shop_supplies
from app.models.user import User
from app.schemas.supplies import Supplies, SuppliesBase, SuppliesCreate, SuppliesUpdate, SuppliesCreateAndAdd
from app.schemas.shop_supplies import ShopSuppliesCreate
from app.dependencies import get_current_user, get_current_admin_user
from datetime import datetime
from typing import List
from app.models.supplies import Category

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Supplies)  # Ensure this uses the Pydantic schema
def create_supplies(supplies: SuppliesCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    return crud_supplies.create_supplies(db=db, supplies=supplies)

@router.post("/createAndAdd", response_model=Supplies)  # Ensure this uses the Pydantic schema
def create_supplies_and_add_to_shop(supplies: SuppliesCreateAndAdd, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    # Create the supply using only SuppliesCreate fields
    created_supply = crud_supplies.create_supplies(
        db=db,
        supplies=SuppliesCreate(
            name=supplies.name,
            purchase_price=supplies.purchase_price,
            size_weight=supplies.size_weight,
            producer=supplies.producer,
            category_id=supplies.category_id,
            image_url=supplies.image_url or "data:image/jpeg;base64,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"
        )
    )
    
    # Add the supply to the shop using ShopSuppliesCreate fields
    shop_supplies_data = ShopSuppliesCreate(
        shop_id=supplies.shop_id,
        supply_id=created_supply.supply_id,
        sale_price=supplies.sale_price,  # Ensure this is part of ShopSuppliesCreate, not SuppliesCreate
        quantity=supplies.quantity,
        delivery_date=datetime.now().strftime("%Y-%m-%d")
    )
    crud_shop_supplies.create_shop_supplies(db=db, shop_supplies=shop_supplies_data)
    
    return created_supply

@router.get("/{supply_id}", response_model=Supplies)  # Ensure this uses the Pydantic schema
def read_supplies(supply_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_supplies = crud_supplies.get_supplies(db, supply_id=supply_id)
    if db_supplies is None:
        raise HTTPException(status_code=404, detail="Supplies not found")
    return db_supplies

@router.put("/{supply_id}", response_model=Supplies)  # Ensure this uses the Pydantic schema
def update_supplies(supply_id: int, supplies: SuppliesUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_supplies = crud_supplies.update_supplies(db, supply_id=supply_id, supplies=supplies)
    if db_supplies is None:
        raise HTTPException(status_code=404, detail="Supplies not found")
    return db_supplies

def get_all_child_category_ids(db: Session, parent_id: int) -> List[int]:
    """
    Recursively fetch all child category IDs for a given parent category ID.
    """
    child_ids = []
    child_categories = db.query(Category).filter(Category.parent_id == parent_id).all()
    for child in child_categories:
        child_ids.append(child.category_id)
        child_ids.extend(get_all_child_category_ids(db, child.category_id))
    return child_ids

@router.get("/shop/{shop_id}/{category_id}", response_model=List[dict])
def get_supplies_by_shop_id(shop_id: int, category_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Fetch combined information from supplies and shop_supplies tables for a specific shop_id.
    """

    category_ids = [category_id] + get_all_child_category_ids(db, category_id)
    
    query = db.query(
        crud_supplies.Supplies.supply_id,  # Include supply_id
        crud_supplies.Supplies.name,
        crud_supplies.Supplies.purchase_price,
        crud_supplies.Supplies.size_weight,
        crud_supplies.Supplies.producer,
        crud_supplies.Supplies.category_id,
        crud_shop_supplies.ShopSupplies.quantity,
        crud_shop_supplies.ShopSupplies.sale_price,
        crud_supplies.Supplies.image_url,
    ).join(
        crud_shop_supplies.ShopSupplies,
        crud_supplies.Supplies.supply_id == crud_shop_supplies.ShopSupplies.supply_id
    ).filter(
        crud_shop_supplies.ShopSupplies.shop_id == shop_id,
        crud_supplies.Supplies.category_id.in_(category_ids)  # Filter by category_ids
    ).all()

    if not query:
        return []

    # Convert tuples to dictionaries
    result = [
        {
            "supply_id": row[0],
            "name": row[1],
            "purchase_price": row[2],
            "size_weight": row[3],
            "producer": row[4],
            "category_id": row[5],
            "quantity": row[6],
            "sale_price": row[7],
            "image_url": row[8],
        }
        for row in query
    ]

    return result

@router.get("/notInShop/{shop_id}/{category_id}", response_model=List[Supplies])  # Ensure this uses the Pydantic schema
def get_all_supplies(shop_id: int, category_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    category_ids = [category_id] + get_all_child_category_ids(db, category_id)  # Fetch category IDs including children

    supplies = db.query(crud_supplies.Supplies).filter(
        ~crud_supplies.Supplies.supply_id.in_(
            db.query(crud_shop_supplies.ShopSupplies.supply_id).filter(
                crud_shop_supplies.ShopSupplies.shop_id == shop_id
            )
        ),
        crud_supplies.Supplies.category_id.in_(category_ids)  # Filter by category_ids
    ).all()

    if not supplies:
        return []
    return supplies
from sqlalchemy.orm import Session, joinedload  # Import for eager loading
from app.models.supplies import Supplies
from app.schemas.supplies import SuppliesCreate, SuppliesUpdate

def create_supplies(db: Session, supplies: SuppliesCreate):
    db_supplies = Supplies(**supplies.dict())
    db.add(db_supplies)
    db.commit()
    db.refresh(db_supplies)
    return db_supplies

def get_supplies(db: Session, supply_id: int):
    return db.query(Supplies).options(joinedload(Supplies.category)).filter(Supplies.supply_id == supply_id).first()
    # Added joinedload to preload related category data

def get_all_supplies(db: Session):
    return db.query(Supplies).options(joinedload(Supplies.category)).all()
    # Added joinedload to preload related category data

def update_supplies(db: Session, supply_id: int, supplies: SuppliesUpdate):
    db_supplies = db.query(Supplies).filter(Supplies.supply_id == supply_id).first()
    if db_supplies:
        for key, value in supplies.dict().items():
            setattr(db_supplies, key, value)
        db.commit()
        db.refresh(db_supplies)
    return db_supplies

def delete_supplies(db: Session, supply_id: int):
    db_supplies = db.query(Supplies).filter(Supplies.supply_id == supply_id).first()
    if db_supplies:
        db.delete(db_supplies)
        db.commit()
    return db_supplies

def get_supply_name_by_id(db: Session, supply_id: int) -> str:
    supply = db.query(Supplies).filter(Supplies.supply_id == supply_id).first()
    if not supply:
        raise ValueError(f"No supply found for supply_id={supply_id}")
    return supply.name
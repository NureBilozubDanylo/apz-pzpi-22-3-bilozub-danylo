from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.supplies import Category, Supplies
from app.dependencies import get_current_user
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/children/{parent_id}", response_model=List[dict])
def get_child_categories(parent_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    child_categories = db.query(Category).filter(Category.parent_id == parent_id).all()
    if not child_categories:
        return []
    
    # Convert SQLAlchemy objects to dictionaries
    return [{"id": category.category_id, "name": category.name, "parent_id": category.parent_id} for category in child_categories]
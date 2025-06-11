from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import employee as crud_employee
from app.schemas.employee import Employee, EmployeeCreate, EmployeeUpdate
from app.dependencies import get_current_admin_user
from app.models.user import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Employee)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    return crud_employee.create_employee(db=db, employee=employee)

@router.get("/{user_id}", response_model=Employee)
def read_employee(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_employee = crud_employee.get_employee(db, user_id=user_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@router.put("/{user_id}", response_model=Employee)
def update_employee(user_id: int, employee: EmployeeUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_employee = crud_employee.update_employee(db, user_id=user_id, employee=employee)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@router.delete("/{user_id}", response_model=Employee)
def delete_employee(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_employee = crud_employee.delete_employee(db, user_id=user_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


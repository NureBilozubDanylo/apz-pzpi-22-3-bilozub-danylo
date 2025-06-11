from sqlalchemy.orm import Session
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate

def create_employee(db: Session, employee: EmployeeCreate) -> Employee:
    db_employee = Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def get_employee(db: Session, user_id: int) -> Employee:
    return db.query(Employee).filter(Employee.user_id == user_id).first()

def update_employee(db: Session, user_id: int, employee: EmployeeUpdate) -> Employee:
    db_employee = db.query(Employee).filter(Employee.user_id == user_id).first()
    if db_employee:
        for key, value in employee.dict(exclude_unset=True).items():
            setattr(db_employee, key, value)
        db.commit()
        db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, user_id: int) -> Employee:
    db_employee = db.query(Employee).filter(Employee.user_id == user_id).first()
    if db_employee:
        db.delete(db_employee)
        db.commit()
    return db_employee

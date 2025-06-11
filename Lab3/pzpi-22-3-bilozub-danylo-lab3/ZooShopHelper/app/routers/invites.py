from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.employee import Employee
from app.database import SessionLocal
from app.models.request import Request
from app.models.shop import Shop
from app.schemas.invites import InviteResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{user_id}", response_model=list[InviteResponse])
def get_user_invites(user_id: int, db: Session = Depends(get_db)):
    # Fetch all requests for the user
    requests = db.query(Request).filter(Request.user_id == user_id).all()
    if not requests:
        raise HTTPException(status_code=404, detail="No invites found for this user")

    # Prepare the response with shop information
    invites = []
    for req in requests:
        shop = db.query(Shop).filter(Shop.shop_id == req.shop_id).first()
        if not shop:
            raise HTTPException(status_code=404, detail=f"Shop with id {req.shop_id} not found")
        invites.append({
            "request_id": req.request_id,
            "user_id": req.user_id,
            "shop_id": req.shop_id,
            "shop_name": shop.name,
            "shop_location": shop.location,
            "message": req.message,
            "status": req.status,
            "work_schedule": shop.work_schedule,
        })
    return invites

@router.post("/accept/{request_id}/{status}")
def update_request_status(request_id: int, status: bool, db: Session = Depends(get_db)):
    # Fetch the request by request_id
    request = db.query(Request).filter(Request.request_id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    # Update the status based on the provided status
    request.status = "approved" if status else "rejected"
    db.commit()
    db.refresh(request)

    # If status is approved, update the shop_id in the Employee table
    if status:
        employee = db.query(Employee).filter(Employee.user_id == request.user_id).first()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found for the given user_id")
        employee.shop_id = request.shop_id
        db.commit()
        db.refresh(employee)

    return {"message": "Request status updated successfully", "request_id": request_id, "new_status": request.status}

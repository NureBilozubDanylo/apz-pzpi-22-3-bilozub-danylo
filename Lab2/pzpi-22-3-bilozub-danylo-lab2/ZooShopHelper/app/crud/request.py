from sqlalchemy.orm import Session
from app.models.request import Request
from app.schemas.request import RequestCreate

def create_request(db: Session, request_data: RequestCreate):
    db_request = Request(**request_data.dict())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

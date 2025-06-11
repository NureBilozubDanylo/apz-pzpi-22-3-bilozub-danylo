from pydantic import BaseModel
from enum import Enum

class RequestStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class RequestCreate(BaseModel):
    message: str
    user_id: int
    shop_id: int

class RequestResponse(BaseModel):
    request_id: int
    message: str
    status: RequestStatus
    user_id: int
    shop_id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel
from datetime import datetime

class InviteResponse(BaseModel):
    request_id: int
    user_id: int
    shop_id: int
    shop_name: str
    shop_location: str
    work_schedule: str
    message: str
    status: str

    class Config:
        orm_mode = True

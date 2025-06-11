from pydantic import BaseModel
from datetime import datetime

class NotificationBase(BaseModel):
    user_id: int
    message: str
    timestamp: datetime
    model_config = {
        "from_attributes": True
    }

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(NotificationBase):
    pass

class Notification(NotificationBase):
    notification_id: int

    model_config = {
        "from_attributes": True
    }
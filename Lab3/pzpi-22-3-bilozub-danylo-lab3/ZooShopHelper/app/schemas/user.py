from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel, EmailStr
class UserBase(BaseModel):
    username: str
    role: str
    email: str
    mobile_number: str
    age: int
    model_config = {
        "from_attributes": True
    }

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    role: str
    model_config = {
        "from_attributes": True
    }

class User(UserBase):
    user_id: int

    model_config = {
        "from_attributes": True
    }

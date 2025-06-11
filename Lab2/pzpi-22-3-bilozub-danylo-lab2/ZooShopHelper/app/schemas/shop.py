from pydantic import BaseModel

class ShopBase(BaseModel):
    name: str
    location: str
    work_schedule: str
    user_id: int
    model_config = {
        "from_attributes": True
    }

class ShopCreate(ShopBase):
    pass

class ShopUpdate(ShopBase):
    pass

class Shop1(ShopBase):
    shop_id: int

    model_config = {
        "from_attributes": True
    }

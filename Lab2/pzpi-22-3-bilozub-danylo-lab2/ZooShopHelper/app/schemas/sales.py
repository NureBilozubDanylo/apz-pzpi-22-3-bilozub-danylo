from pydantic import BaseModel
from datetime import date
from typing import List

class SalesBase(BaseModel):
    sale_date: date
    pay_type: str

class SalesCreate(SalesBase):
    user_id: int

class Sales(SalesBase):
    id: int
    user_id: int

    model_config = {
        "from_attributes": True
    }

class Product(BaseModel):
    supply_id: int
    count: int
    sale_price: float

class SaleConfirmation(BaseModel):
    shop_id: int
    products: List[Product]
    paymentType: str

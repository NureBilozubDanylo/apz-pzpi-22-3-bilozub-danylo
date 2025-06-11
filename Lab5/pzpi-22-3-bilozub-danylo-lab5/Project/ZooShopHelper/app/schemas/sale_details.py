from pydantic import BaseModel
from typing import Optional

class SaleDetailsBase(BaseModel):
    sale_id: int
    shop_supplies_id: int
    quantity: int
    total_price: float

class SaleDetailsCreate(SaleDetailsBase):
    pass

class SaleDetails(SaleDetailsBase):
    sale_details_id: int

    model_config = {
        "from_attributes": True
    }

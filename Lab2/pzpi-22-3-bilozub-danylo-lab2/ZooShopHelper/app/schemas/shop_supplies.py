from pydantic import BaseModel

class ShopSuppliesBase(BaseModel):
    shop_id: int
    supply_id: int
    quantity: int
    sale_price: float
    model_config = {
        "from_attributes": True
    }

class ShopSuppliesCreate(ShopSuppliesBase):
    sale_price: float
    pass

class ShopSuppliesUpdate(ShopSuppliesBase):
    pass

class DeductSupply(BaseModel):
    shop_id: int
    supply_id: int
    quantity: int

class ShopSupplies(ShopSuppliesBase):
    shop_supplies_id: int

    model_config = {
        "from_attributes": True
    }
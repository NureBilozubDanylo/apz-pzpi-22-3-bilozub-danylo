from sqlalchemy import Column, Integer, ForeignKey, Float, DECIMAL
from app.database import Base

class SaleDetails(Base):
    __tablename__ = "SaleDetails"
    sale_details_id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.sale_id"))
    shop_supplies_id = Column(Integer, ForeignKey("ShopSupplies.shop_supplies_id"))
    quantity = Column(Integer, nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=False)

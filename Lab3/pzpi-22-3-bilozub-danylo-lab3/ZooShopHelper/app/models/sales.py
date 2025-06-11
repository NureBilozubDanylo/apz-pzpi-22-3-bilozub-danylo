from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Sales(Base):
    __tablename__ = "sales"

    sale_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.user_id"))
    shop_id = Column(Integer, ForeignKey("Shop.shop_id"))
    sale_date = Column(Date, nullable=False)
    pay_type = Column(String(30), nullable=False)

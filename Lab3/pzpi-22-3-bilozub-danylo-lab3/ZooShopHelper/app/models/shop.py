from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Shop(Base):
    __tablename__ = "Shop"
    shop_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    location = Column(String)
    work_schedule = Column(String)
    user_id = Column(Integer, ForeignKey("Users.user_id"))
    requests = relationship("Request", back_populates="shop", cascade="all, delete-orphan")

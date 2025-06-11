from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base


class Request(Base):
    __tablename__ = "requests"

    request_id = Column(Integer, primary_key=True, index=True)
    message = Column(String, nullable=False)
    status = Column(String, default="pending")
    user_id = Column(Integer, ForeignKey("Users.user_id"), nullable=False)
    shop_id = Column(Integer, ForeignKey("Shop.shop_id"), nullable=False)
    user = relationship("User", back_populates="requests")
    shop = relationship("Shop", back_populates="requests")
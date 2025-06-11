from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.user import User
from app.database import Base

class Employee(Base):
    __tablename__ = "Employees"
    user_id = Column(Integer, ForeignKey("Users.user_id"), primary_key=True)
    shop_id = Column(Integer, ForeignKey("Shop.shop_id"))
    position = Column(String)
    salary_without_percent = Column(Integer)

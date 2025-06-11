from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "Users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)
    email = Column(String)
    mobile_number = Column(String)
    age = Column(Integer)
    requests = relationship("Request", back_populates="user", cascade="all, delete-orphan")

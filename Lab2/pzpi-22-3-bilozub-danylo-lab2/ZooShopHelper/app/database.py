from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine("postgresql+psycopg2://postgres:Danya123@localhost:5432/ZooShopHelper")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

Base.metadata.create_all(engine)
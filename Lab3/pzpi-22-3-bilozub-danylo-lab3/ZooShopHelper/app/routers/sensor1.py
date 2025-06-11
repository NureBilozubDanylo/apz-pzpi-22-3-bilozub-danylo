from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.sensor import Sensor1, SensorCreate
from app.crud import sensor as crud_sensor
from app.models.user import User
from app.dependencies import get_current_user, get_current_admin_user

router = APIRouter(
    prefix="/sensor",
    tags=["Sensors"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------  створення сенсора  -----------------
@router.post("/", response_model=Sensor1)
def create_sensor(
    sensor: SensorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)  # тільки для адміністраторів
):
    return crud_sensor.create_sensor(db, sensor)

# ---------  отримати всі сенсори певного магазину  -------
@router.get("/shop/{shop_id}/sensors", response_model=List[Sensor1])
def get_sensors_by_shop(
    shop_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # будь-який авторизований
):
    sensors = crud_sensor.get_sensors_by_shop_id(db, shop_id)
    if not sensors:
        raise HTTPException(status_code=404, detail="No sensors found")
    return sensors

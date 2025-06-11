from fastapi import FastAPI, Request
from psycopg2 import connect
from app.database import engine, Base
from app.database import SessionLocal 
from app.crud.user import create_user, get_user
from app.schemas.user import UserCreate
from app.models import user
from app.models import animal
from app.models import climate_history
from app.models import climate_settings
from app.models import shop
from app.models import notification
from app.models import sensor
from app.models import shop_supplies
from app.models import supplies
from app.models import user_in_shop
from fastapi_utils.tasks import repeat_every
from app.crud.animal import check_feeding_times
import threading
from app.backup import backup_database
from fastapi.middleware.cors import CORSMiddleware

from app.routers import animal, user, climate_settings, climate_history, notifications, sensor, shop_supplies, shop, user_in_shop, supplies, auth, categories, employee, sales
from app.routers import sale_details
from app.routers import invites
from app.routers import sensor1
from app.routers import admin_tools
from app.routers import admin_management

import logging
from pathlib import Path

LOG_PATH = Path("server.log")      # такий самий, як у admin_management.py

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
        logging.StreamHandler()          # щоб писало і в консоль
    ]
)

# приклад тест-логу при запуску
logging.getLogger("startup").info("Server starting…")

app = FastAPI()
app.include_router(animal.router, prefix="/animals", tags=["Animals"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(climate_settings.router, prefix="/climate_settings", tags=["Climate_settings"])
app.include_router(climate_history.router, prefix="/climate_history", tags=["Climate_history"])
app.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
app.include_router(sensor.router, prefix="/sensors", tags=["Sensors"])
app.include_router(shop_supplies.router, prefix="/shop_supplies", tags=["Shop_supplies"])
app.include_router(shop.router, prefix="/shops", tags=["Shops"])
app.include_router(user_in_shop.router, prefix="/user_in_shop", tags=["User_in_shop"])
app.include_router(supplies.router, prefix="/supplies", tags=["Supplies"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(employee.router, prefix="/employees", tags=["Employees"])
app.include_router(sales.router, prefix="/sales", tags=["sales"])
app.include_router(sale_details.router)
app.include_router(invites.router, prefix="/invites", tags=["Invites"])
app.include_router(sensor1.router)
app.include_router(admin_tools.router)
app.include_router(admin_management.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Укажите источник, с которого разрешены запросы
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

@app.post("/api/data")
async def receive_data(request: Request):
    data = await request.json()
    print("Received data:", data)
    return {"status": "success"}

@app.get("/") 
def read_root(): 
    return {"message": "Welcome to the API"}

Base.metadata.create_all(engine)

# new_user_data = UserCreate(
#     username="алло123123",
#     password="testptass",
#     role="admin",
#     email="test@example.com",
#     mobile_number="1234567890",
#     age=30
# )

# db = SessionLocal()
# new_user = create_user(db, new_user_data) 
# user = get_user(db, user_id=1) 
# print(user)
# db.close()

def start_backup_scheduler():
    import schedule
    import time

    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)

    schedule.every().day.at("02:00").do(backup_database)
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

@app.on_event("startup")
@repeat_every(seconds=600)  # 10 minutes
def periodic_feeding_check():
    db = SessionLocal()
    try:
        check_feeding_times(db)
    finally:
        db.close()

@app.on_event("startup")
def on_startup():
    start_backup_scheduler()


import random
from datetime import datetime
from fastapi_utils.tasks import repeat_every
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import sensor as crud_sensor
from app.models.climate_settings import ClimateSettings
from app.models.sensor import Sensor
from app.schemas.sensor import Sensor1,SensorBase, SensorCreate, SensorUpdate
from app.models.user import User
from app.dependencies import get_current_user, get_current_admin_user
from app.crud import climate_history as crud_climate_history
from app.schemas.climate_history import ClimateHistoryCreate
from app.crud import notification as crud_notification
from app.schemas.notification import NotificationCreate
from app.crud import user_in_shop as crud_user_in_shop
from typing import List
# ─────────────────────────────────────────────
# logging – налаштовуємо на початку main.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("sensor_simulator")
# ─────────────────────────────────────────────


# ------------------- helpers -------------------
def random_value(sensor_type: str) -> float:
    if sensor_type == "temperature":
        return round(random.uniform(18, 35), 1)
    if sensor_type == "humidity":
        return round(random.uniform(30, 85), 1)
    if sensor_type == "light_intensity":
        return round(random.uniform(50, 900), 1)
    return 0.0


# ------------------- periodic task --------------
@app.on_event("startup")          # ❶ ОБОВʼЯЗКОВО
@repeat_every(seconds=10, raise_exceptions=False, wait_first=True)
def simulate_sensors() -> None:
    """
    Раз у 5 с оновлює ВСІ сенсори, перевіряє відхилення,
    пише ClimateHistory та Notifications.
    """
    db: Session = SessionLocal()
    try:
        sensors = db.query(Sensor).all()
        if not sensors:
            log.info("No sensors in DB → nothing to simulate")
            return

        # 1️⃣ генеруємо нові значення
        for s in sensors:
            new_val = random_value(s.type)
            log.info("Sensor %s (%s) → %s", s.sensor_id, s.type, new_val)
            s.current_value = new_val
        db.commit()

        # 2️⃣ групуємо по магазинах
        shops: dict[int, list[Sensor]] = {}
        for s in sensors:
            shops.setdefault(s.shop_id, []).append(s)

        for shop_id, shop_sensors in shops.items():
            cs = db.query(ClimateSettings).filter(
                ClimateSettings.shop_id == shop_id
            ).first()

            # --- перевірка відхилень та нотифікації ---
            for s in shop_sensors:
                warn_msg = None
                if cs:
                    if s.type == "temperature" and abs(s.current_value - cs.temperature) > 3:
                        warn_msg = f"⚠ Temp {s.current_value}°C but normal is {cs.temperature}°C"
                    elif s.type == "humidity" and abs(s.current_value - cs.humidity) > 5:
                        warn_msg = f"⚠ Hum {s.current_value}% but normal is {cs.humidity}%"
                    elif s.type == "light_intensity" and abs(s.current_value - cs.light_intensity) > 50:
                        warn_msg = f"⚠ Light {s.current_value}lx but normal is {cs.light_intensity}lx"

                if warn_msg:
                    log.warning("Shop %s: %s", shop_id, warn_msg)
                    users = crud_user_in_shop.get_users_in_shop_by_shop_id(db, shop_id=shop_id)
                    for u in users:
                        note = NotificationCreate(
                            user_id=u.user_id,
                            message=warn_msg,
                            timestamp=datetime.utcnow()
                        )
                        crud_notification.create_notification(db=db, notification=note)

            # --- запис у ClimateHistory ---
            t = h = l = None
            for s in shop_sensors:
                if s.type == "temperature":
                    t = s.current_value
                elif s.type == "humidity":
                    h = s.current_value
                elif s.type == "light_intensity":
                    l = s.current_value
            history = ClimateHistoryCreate(
                temperature=t,
                humidity=h,
                light_intensity=l,
                record_date=datetime.utcnow(),
                shop_id=shop_id
            )
            crud_climate_history.create_climate_history(db=db, climate_history=history)

        db.commit()
        log.info("Simulation cycle finished ✔")
    except Exception as e:
        log.exception("Error in simulate_sensors: %s", e)
    finally:
        db.close()
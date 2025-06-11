"""
Адміністративні інструменти:
  • System Admin   – конфіги, стани, логи
  • Platform Admin – керування користувачами / компаніями
  • DB Admin       – резервні копії, оптимізація БД
"""

import os, time, json, shutil, subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import psutil
import psycopg2
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine
from app.dependencies import get_current_admin_user
from app.crud import user as crud_user
from app.schemas.user import UserUpdate
from app.backup import backup_database
from app.dependencies import get_current_admin_user
from app.models.user import User

router = APIRouter(prefix="/admin", tags=["Admin"])

SYSTEM_CONFIG: Dict[str, str | int | bool] = {
    "default_locale": "en",
    "max_file_size_mb": 50,
}
START_TIME = time.time()

LOG_PATH = Path("server.log")
START_TS = time.time()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def as_admin(user=Depends(get_current_admin_user)):
    return user

@router.post("/backup")
def manual_backup(current: User = Depends(get_current_admin_user)):
    """Ручне резервне копіювання."""
    try:
        backup_database()        # існуюча функція
        return {"status": "ok", "timestamp": datetime.utcnow()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
def server_stats(current: User = Depends(get_current_admin_user)):
    """Повертає аптайм, CPU %, RAM та диск."""
    uptime = time.time() - START_TIME
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    return {
        "uptime_sec": int(uptime),
        "cpu_percent": psutil.cpu_percent(interval=0.2),
        "ram_used_mb": int(mem.used / 1024 / 1024),
        "ram_total_mb": int(mem.total / 1024 / 1024),
        "disk_used_gb": round(disk.used / 1024**3, 1),
        "disk_total_gb": round(disk.total / 1024**3, 1),
    }


@router.get("/system/status")
def system_status(_: str = Depends(as_admin)):
    """CPU, RAM, диск та аптайм."""
    uptime = int(time.time() - START_TS)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    return {
        "uptime_sec": uptime,
        "cpu_percent": psutil.cpu_percent(interval=0.2),
        "ram_used_mb": int(mem.used / 1024 / 1024),
        "ram_total_mb": int(mem.total / 1024 / 1024),
        "disk_used_gb": round(disk.used / 1024**3, 1),
        "disk_total_gb": round(disk.total / 1024**3, 1),
        "config": SYSTEM_CONFIG,
    }

@router.get("/system/config")
def get_config(_: str = Depends(as_admin)):
    return SYSTEM_CONFIG

@router.put("/system/config")
def update_config(changes: Dict[str, str | int | bool], _: str = Depends(as_admin)):
    SYSTEM_CONFIG.update(changes)
    return {"status": "updated", "config": SYSTEM_CONFIG}

@router.get("/system/logs")
def get_logs(lines: int = 200, _: str = Depends(as_admin)):
    """Повернути останні N рядків лог-файлу."""
    if not LOG_PATH.exists():
        raise HTTPException(404, "log file not found")
    with LOG_PATH.open("r", encoding="utf-8", errors="ignore") as f:
        data = f.readlines()[-lines:]
    return {"log": "".join(data)}

@router.delete("/system/logs")
def clear_logs(_: str = Depends(as_admin)):
    if LOG_PATH.exists():
        LOG_PATH.write_text("")
    return {"status": "cleared"}



BACKUP_DIR = Path("db_backups")
BACKUP_DIR.mkdir(exist_ok=True)

@router.post("/db/backup")
def create_backup(_: str = Depends(as_admin)):
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    backup_database()
    return {"status": "backup_created", "timestamp": ts}

@router.post("/db/restore")
def restore_backup(file: UploadFile = File(...),
                   _: str = Depends(as_admin)):
    """Приймає *.sql.gz або *.dump та відновлює БД."""
    dst = BACKUP_DIR / file.filename
    with dst.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    cmd = f'psql "{os.getenv("DATABASE_URL")}" -f "{dst}"'
    subprocess.run(cmd, shell=True, check=True)
    return {"status": "restored", "file": file.filename}

@router.get("/db/status")
def db_status(_: str = Depends(as_admin)):
    with engine.connect() as conn:
        results = conn.execute(text("""
            SELECT
                table_name,
                pg_total_relation_size(quote_ident(table_name)) AS size
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """)).fetchall()

    total = sum(row.size for row in results)
    return {
        "tables": [{ "name": row.table_name, "size_bytes": row.size } for row in results],
        "total_size_mb": round(total / 1024 / 1024, 2),
    }

@router.post("/db/optimize")
def optimize_db(_: str = Depends(as_admin)):
    conn = engine.raw_connection()
    try:
        conn.set_session(autocommit=True)
        cur = conn.cursor()
        cur.execute("VACUUM")
        cur.close()
    finally:
        conn.close()
    return {"status": "vacuum_ok"}

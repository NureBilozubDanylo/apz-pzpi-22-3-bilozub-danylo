from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
from pathlib import Path
import psutil, os, shutil, time

from app.dependencies import get_current_admin_user
from app.models.user import User
from app.backup import backup_database    # функція вже існує

router = APIRouter(prefix="/admin", tags=["Admin"])

# для аптайму
START_TIME = time.time()

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

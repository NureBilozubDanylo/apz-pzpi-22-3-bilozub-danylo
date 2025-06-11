from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
from pathlib import Path
import psutil, os, shutil, time
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
from app.dependencies import get_current_admin_user
from app.models.user import User
from app.backup import backup_database   

router = APIRouter(prefix="/admin", tags=["Admin"])

# для аптайму
START_TIME = time.time()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def as_admin(user=Depends(get_current_admin_user)):
    return user

@router.put("/platform/users/{user_id}/role")
def set_user_role(user_id: int, new_role: str = Form(...),
                  db: Session = Depends(get_db),
                  _: str = Depends(as_admin)):
    if new_role not in {"worker", "director", "admin"}:
        raise HTTPException(400, "invalid role")
    crud_user.update_user(db, user_id, UserUpdate(role=new_role))
    return {"status": "ok", "user_id": user_id, "role": new_role}

@router.post("/platform/users/{user_id}/logout")
def force_logout(user_id: int, db: Session = Depends(get_db), _: str = Depends(as_admin)):
    user = crud_user.get_user(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    user.token = None
    db.commit()
    return {"status": "force_logged_out", "user_id": user_id}

@router.delete("/platform/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), _: str = Depends(as_admin)):
    user = crud_user.get_user(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    db.execute(text("DELETE FROM \"Employees\" WHERE user_id = :uid"), {"uid": user_id})
    db.commit()

    db.delete(user)
    db.commit()

    return {"status": "deleted", "user_id": user_id}

@router.patch("/platform/users/{user_id}/role")
def change_user_role(
    user_id: int,
    new_role: str = Form(...),
    db: Session = Depends(get_db),
    _: str = Depends(as_admin)
):
    if new_role not in {"worker", "director", "admin"}:
        raise HTTPException(400, "Invalid role")
    crud_user.update_user(db, user_id, UserUpdate(role=new_role))
    return {"status": "updated", "user_id": user_id, "new_role": new_role}
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.settings import SettingsResponse, SettingsUpdate
from app.services import settings as settings_service

router = APIRouter()


@router.get("", response_model=SettingsResponse)
def get_settings(db: Session = Depends(get_db)):
    return settings_service.get_settings(db)


@router.patch("", response_model=SettingsResponse)
def update_settings(payload: SettingsUpdate, db: Session = Depends(get_db)):
    return settings_service.update_settings(db, payload.model_dump())

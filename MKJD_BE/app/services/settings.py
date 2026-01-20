from sqlalchemy.orm import Session

from app.core.config import settings as app_settings
from app.db.models.settings import Settings

DEFAULT_SETTINGS_ID = "default"


def get_settings(db: Session) -> Settings:
    instance = db.get(Settings, DEFAULT_SETTINGS_ID)
    if instance:
        return instance

    instance = Settings(
        id=DEFAULT_SETTINGS_ID,
        threshold_low=app_settings.threshold_low,
        threshold_high=app_settings.threshold_high,
        borderline_enabled=app_settings.borderline_enabled,
        monitored_videos=[],
        language="id",
        theme="light",
        density="standard",
        notify_new_comments=True,
        auto_hold_suspicious=True,
    )
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def update_settings(db: Session, patch: dict) -> Settings:
    instance = get_settings(db)
    for key, value in patch.items():
        if hasattr(instance, key) and value is not None:
            setattr(instance, key, value)
    db.commit()
    db.refresh(instance)
    return instance

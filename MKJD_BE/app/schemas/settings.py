from typing import Optional

from app.schemas.common import APIModel


class SettingsResponse(APIModel):
    threshold_low: float
    threshold_high: float
    borderline_enabled: bool
    monitored_videos: Optional[list[str]] = None
    language: str
    theme: str
    density: str
    notify_new_comments: bool
    auto_hold_suspicious: bool


class SettingsUpdate(APIModel):
    threshold_low: Optional[float] = None
    threshold_high: Optional[float] = None
    borderline_enabled: Optional[bool] = None
    monitored_videos: Optional[list[str]] = None
    language: Optional[str] = None
    theme: Optional[str] = None
    density: Optional[str] = None
    notify_new_comments: Optional[bool] = None
    auto_hold_suspicious: Optional[bool] = None

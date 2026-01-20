from sqlalchemy import Boolean, Column, DateTime, Float, JSON, String
from sqlalchemy.sql import func

from app.db.base import Base


class Settings(Base):
    __tablename__ = "settings"

    id = Column(String(64), primary_key=True)
    threshold_low = Column(Float, default=0.4)
    threshold_high = Column(Float, default=0.7)
    borderline_enabled = Column(Boolean, default=True)
    monitored_videos = Column(JSON)
    language = Column(String(16), default="id")
    theme = Column(String(32), default="light")
    density = Column(String(32), default="standard")
    notify_new_comments = Column(Boolean, default=True)
    auto_hold_suspicious = Column(Boolean, default=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

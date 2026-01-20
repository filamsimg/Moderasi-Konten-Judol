from sqlalchemy import Boolean, Column, DateTime, Enum, String, Text
from sqlalchemy.sql import func

from app.db.base import Base
from app.db.models.enums import TargetType


class MonitoringTarget(Base):
    __tablename__ = "monitoring_targets"

    id = Column(String(64), primary_key=True)
    type = Column(Enum(TargetType, native_enum=False), nullable=False)
    label = Column(String(255), nullable=False)
    target = Column(String(128), nullable=False, index=True)
    filter = Column(Text)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

from sqlalchemy import Column, DateTime, Enum, Float, Integer, String
from sqlalchemy.sql import func

from app.db.base import Base
from app.db.models.enums import PipelineState


class PipelineStatus(Base):
    __tablename__ = "pipeline_status"

    id = Column(String(64), primary_key=True)
    status = Column(Enum(PipelineState, native_enum=False), default=PipelineState.PAUSED)
    last_fetch = Column(DateTime(timezone=True))
    avg_latency_sec = Column(Float)
    queue_size = Column(Integer)
    processed_last_hour = Column(Integer)
    error_rate = Column(Float)
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

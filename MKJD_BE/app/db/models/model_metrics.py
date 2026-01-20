from sqlalchemy import Boolean, Column, DateTime, Float, String
from sqlalchemy.sql import func

from app.db.base import Base


class ModelMetrics(Base):
    __tablename__ = "model_metrics"

    id = Column(String(64), primary_key=True)
    model_name = Column(String(128), nullable=False)
    version = Column(String(64), nullable=False)
    precision = Column(Float)
    recall = Column(Float)
    f1 = Column(Float)
    pr_auc = Column(Float)
    avg_latency_ms = Column(Float)
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

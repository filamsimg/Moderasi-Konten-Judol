from datetime import datetime
from typing import Optional

from app.schemas.common import APIModel


class ModelMetricsBase(APIModel):
    id: str
    model_name: str
    version: str
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1: Optional[float] = None
    pr_auc: Optional[float] = None
    avg_latency_ms: Optional[float] = None
    updated_at: Optional[datetime] = None
    is_active: bool = True


class ModelMetricsCreate(APIModel):
    model_name: str
    version: str
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1: Optional[float] = None
    pr_auc: Optional[float] = None
    avg_latency_ms: Optional[float] = None
    is_active: bool = True


class ModelMetricsResponse(ModelMetricsBase):
    pass


class ModelMetricsListResponse(APIModel):
    items: list[ModelMetricsResponse]
    total: int
    limit: int
    offset: int

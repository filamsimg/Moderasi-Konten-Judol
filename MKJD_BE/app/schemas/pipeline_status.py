from datetime import datetime
from typing import Optional

from app.schemas.common import APIModel, PipelineState


class PipelineStatusResponse(APIModel):
    status: PipelineState
    last_fetch: Optional[datetime] = None
    avg_latency_sec: Optional[float] = None
    queue_size: Optional[int] = None
    processed_last_hour: Optional[int] = None
    error_rate: Optional[float] = None


class PipelineStatusUpdate(APIModel):
    status: Optional[PipelineState] = None
    last_fetch: Optional[datetime] = None
    avg_latency_sec: Optional[float] = None
    queue_size: Optional[int] = None
    processed_last_hour: Optional[int] = None
    error_rate: Optional[float] = None

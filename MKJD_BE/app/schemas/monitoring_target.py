from datetime import datetime
from typing import Optional

from app.schemas.common import APIModel, TargetType


class MonitoringTargetBase(APIModel):
    id: str
    type: TargetType
    label: str
    target: str
    filter: Optional[str] = None
    active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class MonitoringTargetCreate(APIModel):
    type: TargetType
    label: str
    target: str
    filter: Optional[str] = None
    active: bool = True


class MonitoringTargetUpdate(APIModel):
    label: Optional[str] = None
    filter: Optional[str] = None
    active: Optional[bool] = None


class MonitoringTargetResponse(MonitoringTargetBase):
    pass


class MonitoringTargetListResponse(APIModel):
    items: list[MonitoringTargetResponse]
    total: int
    limit: int
    offset: int

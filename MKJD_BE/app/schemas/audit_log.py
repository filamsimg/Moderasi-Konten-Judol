from datetime import datetime
from typing import Optional

from app.schemas.common import APIModel, Decision


class AuditLogBase(APIModel):
    id: str
    at: Optional[datetime] = None
    action: str
    comment_id: Optional[str] = None
    score: Optional[float] = None
    from_decision: Optional[Decision] = None
    to_decision: Optional[Decision] = None
    actor: str
    result: str
    note: Optional[str] = None


class AuditLogCreate(APIModel):
    action: str
    comment_id: Optional[str] = None
    score: Optional[float] = None
    from_decision: Optional[Decision] = None
    to_decision: Optional[Decision] = None
    actor: str
    result: str = "OK"
    note: Optional[str] = None


class AuditLogResponse(AuditLogBase):
    pass


class AuditLogListResponse(APIModel):
    items: list[AuditLogResponse]
    total: int
    limit: int
    offset: int

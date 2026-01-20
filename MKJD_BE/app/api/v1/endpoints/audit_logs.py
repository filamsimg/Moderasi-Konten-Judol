from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.audit_log import AuditLogListResponse
from app.services import audit_logs

router = APIRouter()


@router.get("", response_model=AuditLogListResponse)
def list_logs(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    comment_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    items, total = audit_logs.list_logs(db, limit=limit, offset=offset, comment_id=comment_id)
    return AuditLogListResponse(items=items, total=total, limit=limit, offset=offset)

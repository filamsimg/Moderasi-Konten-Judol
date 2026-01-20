import uuid
from sqlalchemy.orm import Session

from app.db.models.audit_log import AuditLog


def list_logs(db: Session, limit: int, offset: int, comment_id: str | None = None):
    query = db.query(AuditLog)
    if comment_id:
        query = query.filter(AuditLog.comment_id == comment_id)
    total = query.count()
    items = (
        query.order_by(AuditLog.at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return items, total


def create_log(db: Session, payload: dict) -> AuditLog:
    log = AuditLog(id=f"log_{uuid.uuid4().hex}", **payload)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

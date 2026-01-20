import uuid
from sqlalchemy.orm import Session

from app.db.models.monitoring_target import MonitoringTarget


def list_targets(db: Session, limit: int, offset: int):
    total = db.query(MonitoringTarget).count()
    items = (
        db.query(MonitoringTarget)
        .order_by(MonitoringTarget.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return items, total


def create_target(db: Session, payload: dict) -> MonitoringTarget:
    target = MonitoringTarget(id=f"target_{uuid.uuid4().hex}", **payload)
    db.add(target)
    db.commit()
    db.refresh(target)
    return target


def update_target(db: Session, target_id: str, patch: dict) -> MonitoringTarget:
    target = db.get(MonitoringTarget, target_id)
    if not target:
        return None
    for key, value in patch.items():
        if value is not None and hasattr(target, key):
            setattr(target, key, value)
    db.commit()
    db.refresh(target)
    return target


def delete_target(db: Session, target_id: str) -> bool:
    target = db.get(MonitoringTarget, target_id)
    if not target:
        return False
    db.delete(target)
    db.commit()
    return True

import uuid
from sqlalchemy.orm import Session

from app.db.models.model_metrics import ModelMetrics


def list_metrics(db: Session, limit: int, offset: int):
    total = db.query(ModelMetrics).count()
    items = (
        db.query(ModelMetrics)
        .order_by(ModelMetrics.updated_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return items, total


def create_metric(db: Session, payload: dict) -> ModelMetrics:
    metric = ModelMetrics(id=f"model_{uuid.uuid4().hex}", **payload)
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric


def set_active(db: Session, metric_id: str) -> ModelMetrics:
    db.query(ModelMetrics).update({ModelMetrics.is_active: False})
    metric = db.get(ModelMetrics, metric_id)
    if not metric:
        return None
    metric.is_active = True
    db.commit()
    db.refresh(metric)
    return metric

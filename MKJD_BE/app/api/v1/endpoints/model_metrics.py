from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.model_metrics import (
    ModelMetricsCreate,
    ModelMetricsListResponse,
    ModelMetricsResponse,
)
from app.services import model_metrics as metrics_service

router = APIRouter()


@router.get("", response_model=ModelMetricsListResponse)
def list_metrics(
    limit: int = Query(20, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    items, total = metrics_service.list_metrics(db, limit=limit, offset=offset)
    return ModelMetricsListResponse(items=items, total=total, limit=limit, offset=offset)


@router.post("", response_model=ModelMetricsResponse)
def create_metric(payload: ModelMetricsCreate, db: Session = Depends(get_db)):
    return metrics_service.create_metric(db, payload.model_dump())


@router.post("/{metric_id}/activate", response_model=ModelMetricsResponse)
def activate_metric(metric_id: str, db: Session = Depends(get_db)):
    metric = metrics_service.set_active(db, metric_id)
    if not metric:
        raise HTTPException(status_code=404, detail="Model not found")
    return metric

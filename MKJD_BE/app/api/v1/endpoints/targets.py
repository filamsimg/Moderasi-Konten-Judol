from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.monitoring_target import (
    MonitoringTargetCreate,
    MonitoringTargetListResponse,
    MonitoringTargetResponse,
    MonitoringTargetUpdate,
)
from app.services import targets as targets_service

router = APIRouter()


@router.get("", response_model=MonitoringTargetListResponse)
def list_targets(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    items, total = targets_service.list_targets(db, limit=limit, offset=offset)
    return MonitoringTargetListResponse(items=items, total=total, limit=limit, offset=offset)


@router.post("", response_model=MonitoringTargetResponse)
def create_target(payload: MonitoringTargetCreate, db: Session = Depends(get_db)):
    return targets_service.create_target(db, payload.model_dump())


@router.patch("/{target_id}", response_model=MonitoringTargetResponse)
def update_target(target_id: str, payload: MonitoringTargetUpdate, db: Session = Depends(get_db)):
    target = targets_service.update_target(db, target_id, payload.model_dump())
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    return target


@router.delete("/{target_id}")
def delete_target(target_id: str, db: Session = Depends(get_db)):
    ok = targets_service.delete_target(db, target_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Target not found")
    return {"status": "ok"}

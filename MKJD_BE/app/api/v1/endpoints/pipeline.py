from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.pipeline_status import PipelineStatusResponse, PipelineStatusUpdate
from app.services import pipeline as pipeline_service

router = APIRouter()


@router.get("/status", response_model=PipelineStatusResponse)
def get_status(db: Session = Depends(get_db)):
    return pipeline_service.get_pipeline_status(db)


@router.patch("/status", response_model=PipelineStatusResponse)
def update_status(payload: PipelineStatusUpdate, db: Session = Depends(get_db)):
    return pipeline_service.update_pipeline_status(db, payload.model_dump())

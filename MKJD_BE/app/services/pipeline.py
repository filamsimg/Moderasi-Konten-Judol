from sqlalchemy.orm import Session

from app.db.models.pipeline_status import PipelineStatus
from app.db.models.enums import PipelineState

DEFAULT_PIPELINE_ID = "default"


def get_pipeline_status(db: Session) -> PipelineStatus:
    instance = db.get(PipelineStatus, DEFAULT_PIPELINE_ID)
    if instance:
        return instance
    instance = PipelineStatus(id=DEFAULT_PIPELINE_ID, status=PipelineState.PAUSED)
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def update_pipeline_status(db: Session, patch: dict) -> PipelineStatus:
    instance = get_pipeline_status(db)
    for key, value in patch.items():
        if hasattr(instance, key) and value is not None:
            setattr(instance, key, value)
    db.commit()
    db.refresh(instance)
    return instance

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_model_service
from app.schemas.common import APIModel
from app.services import moderation as moderation_service
from app.services import settings as settings_service
from app.services.normalization import normalize_text

router = APIRouter()


class InferenceRequest(APIModel):
    texts: List[str]
    normalize: bool = True


class InferenceResponse(APIModel):
    scores: List[float]
    decisions: List[Optional[str]]


@router.post("", response_model=InferenceResponse)
def run_inference(
    payload: InferenceRequest,
    db: Session = Depends(get_db),
    model_service=Depends(get_model_service),
):
    if model_service is None or not model_service.loaded:
        raise HTTPException(status_code=503, detail="Model service not available")

    texts = payload.texts
    if payload.normalize:
        texts = [normalize_text(text) for text in texts]

    scores = model_service.predict_scores(texts)
    settings = settings_service.get_settings(db)
    decisions = [
        moderation_service.decide(
            score,
            threshold_low=settings.threshold_low,
            threshold_high=settings.threshold_high,
            borderline_enabled=settings.borderline_enabled,
        ).value
        if score is not None
        else None
        for score in scores
    ]

    return InferenceResponse(scores=scores, decisions=decisions)

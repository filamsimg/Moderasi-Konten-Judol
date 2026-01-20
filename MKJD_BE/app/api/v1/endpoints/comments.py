from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.comment import CommentCreate, CommentListResponse, CommentResponse
from app.schemas.common import APIModel, DecisionPayload
from app.services import audit_logs, comments as comments_service, settings as settings_service

router = APIRouter()


class ScorePayload(APIModel):
    score: float
    actor: Optional[str] = None
    note: Optional[str] = None


@router.get("", response_model=CommentListResponse)
def list_comments(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    decision: Optional[str] = None,
    yt_status: Optional[str] = None,
    score_min: Optional[float] = None,
    score_max: Optional[float] = None,
    q: Optional[str] = None,
    db: Session = Depends(get_db),
):
    items, total = comments_service.list_comments(
        db,
        limit=limit,
        offset=offset,
        decision=decision,
        yt_status=yt_status,
        score_min=score_min,
        score_max=score_max,
        query=q,
    )
    return CommentListResponse(items=items, total=total, limit=limit, offset=offset)


@router.post("", response_model=CommentResponse)
def create_comment(payload: CommentCreate, db: Session = Depends(get_db)):
    comment = comments_service.create_comment(db, payload.model_dump())
    return comment


@router.get("/{comment_id}", response_model=CommentResponse)
def get_comment(comment_id: str, db: Session = Depends(get_db)):
    comment = comments_service.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.post("/{comment_id}/decision", response_model=CommentResponse)
def update_decision(
    comment_id: str,
    payload: DecisionPayload,
    db: Session = Depends(get_db),
):
    comment = comments_service.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    from_decision = comment.decision
    comment = comments_service.update_decision(db, comment, payload.decision)

    audit_logs.create_log(
        db,
        {
            "action": "DECISION_UPDATE",
            "comment_id": comment.id,
            "score": comment.score,
            "from_decision": from_decision,
            "to_decision": payload.decision,
            "actor": payload.actor or "admin",
            "result": "OK",
            "note": payload.note or f"Decision updated to {payload.decision}",
        },
    )
    return comment


@router.post("/{comment_id}/score", response_model=CommentResponse)
def apply_score(
    comment_id: str,
    payload: ScorePayload,
    db: Session = Depends(get_db),
):
    comment = comments_service.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    settings = settings_service.get_settings(db)
    from_decision = comment.decision
    comment = comments_service.apply_score(
        db,
        comment,
        payload.score,
        threshold_low=settings.threshold_low,
        threshold_high=settings.threshold_high,
        borderline_enabled=settings.borderline_enabled,
    )

    audit_logs.create_log(
        db,
        {
            "action": "MODEL_SCORE",
            "comment_id": comment.id,
            "score": payload.score,
            "from_decision": from_decision,
            "to_decision": comment.decision,
            "actor": payload.actor or "system",
            "result": "OK",
            "note": payload.note or "Model score applied",
        },
    )
    return comment

from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models.comment import Comment
from app.services.moderation import decide, yt_status_for_decision
from app.services.normalization import normalize_text


def list_comments(
    db: Session,
    limit: int,
    offset: int,
    decision: Optional[str] = None,
    yt_status: Optional[str] = None,
    score_min: Optional[float] = None,
    score_max: Optional[float] = None,
    query: Optional[str] = None,
):
    q = db.query(Comment)
    if decision:
        q = q.filter(Comment.decision == decision)
    if yt_status:
        q = q.filter(Comment.yt_status == yt_status)
    if score_min is not None:
        q = q.filter(Comment.score >= score_min)
    if score_max is not None:
        q = q.filter(Comment.score <= score_max)
    if query:
        q = q.filter(Comment.text_raw.ilike(f"%{query}%"))

    total = q.count()
    items = (
        q.order_by(func.coalesce(Comment.published_at, Comment.fetched_at).desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return items, total


def get_comment(db: Session, comment_id: str) -> Optional[Comment]:
    return db.get(Comment, comment_id)


def create_comment(db: Session, payload: dict) -> Comment:
    existing = db.get(Comment, payload["id"])
    if existing:
        return existing

    text_norm = normalize_text(payload["text_raw"])
    comment = Comment(**payload, text_norm=text_norm)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def apply_score(
    db: Session,
    comment: Comment,
    score: float,
    threshold_low: float,
    threshold_high: float,
    borderline_enabled: bool,
) -> Comment:
    comment.score = score
    decision = decide(score, threshold_low, threshold_high, borderline_enabled)
    comment.decision = decision
    comment.yt_status = yt_status_for_decision(decision)
    db.commit()
    db.refresh(comment)
    return comment


def update_decision(db: Session, comment: Comment, decision) -> Comment:
    comment.decision = decision
    comment.yt_status = yt_status_for_decision(decision)
    db.commit()
    db.refresh(comment)
    return comment

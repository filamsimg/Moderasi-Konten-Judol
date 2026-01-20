from typing import Optional

from app.db.models.enums import Decision, YTStatus


def decide(
    score: Optional[float],
    threshold_low: float,
    threshold_high: float,
    borderline_enabled: bool,
) -> Optional[Decision]:
    if score is None:
        return None
    if score >= threshold_high:
        return Decision.HELD
    if score >= threshold_low:
        return Decision.BORDERLINE if borderline_enabled else Decision.HELD
    return Decision.PUBLISHED


def yt_status_for_decision(decision: Optional[Decision]) -> Optional[YTStatus]:
    if decision == Decision.PUBLISHED:
        return YTStatus.PUBLISHED
    if decision in (Decision.HELD, Decision.BORDERLINE):
        return YTStatus.HELD_FOR_REVIEW
    if decision == Decision.REJECTED:
        return YTStatus.REJECTED
    return None

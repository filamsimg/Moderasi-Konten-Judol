from pydantic import BaseModel, ConfigDict

from app.db.models.enums import Decision, PipelineState, TargetType, YTStatus


class APIModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class HealthResponse(APIModel):
    status: str


class DecisionPayload(APIModel):
    decision: Decision
    actor: str | None = "admin"
    note: str | None = None


__all__ = [
    "APIModel",
    "Decision",
    "PipelineState",
    "TargetType",
    "YTStatus",
    "HealthResponse",
    "DecisionPayload",
]

from fastapi import APIRouter

from app.api.v1.endpoints import (
    audit_logs,
    comments,
    inference,
    model_metrics,
    oauth,
    pipeline,
    settings,
    targets,
)

api_router = APIRouter()

api_router.include_router(comments.router, prefix="/comments", tags=["comments"])
api_router.include_router(audit_logs.router, prefix="/audit-logs", tags=["audit"])
api_router.include_router(targets.router, prefix="/targets", tags=["targets"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
api_router.include_router(oauth.router, prefix="/oauth", tags=["oauth"])
api_router.include_router(model_metrics.router, prefix="/models", tags=["models"])
api_router.include_router(pipeline.router, prefix="/pipeline", tags=["pipeline"])
api_router.include_router(inference.router, prefix="/inference", tags=["inference"])

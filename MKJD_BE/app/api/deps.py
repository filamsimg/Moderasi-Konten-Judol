from fastapi import Request

from app.db.session import get_db


def get_model_service(request: Request):
    return getattr(request.app.state, "model_service", None)

__all__ = ["get_db", "get_model_service"]

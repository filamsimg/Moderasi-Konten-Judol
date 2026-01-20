from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.config import settings
from app.schemas.oauth_account import OAuthStatusResponse, OAuthStatusUpdate
from app.services import oauth as oauth_service

router = APIRouter()


@router.get("/status", response_model=OAuthStatusResponse)
def get_status(db: Session = Depends(get_db)):
    return oauth_service.get_oauth_account(db)


@router.patch("/status", response_model=OAuthStatusResponse)
def update_status(payload: OAuthStatusUpdate, db: Session = Depends(get_db)):
    return oauth_service.update_oauth_account(db, payload.model_dump())


@router.get("/youtube/connect")
def get_connect_url():
    if not settings.youtube_client_id or not settings.youtube_redirect_uri:
        raise HTTPException(status_code=400, detail="YouTube OAuth config missing")

    params = {
        "client_id": settings.youtube_client_id,
        "redirect_uri": settings.youtube_redirect_uri,
        "response_type": "code",
        "access_type": "offline",
        "prompt": "consent",
        "scope": "https://www.googleapis.com/auth/youtube.force-ssl",
    }
    url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    return {"url": url}

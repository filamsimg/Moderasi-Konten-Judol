from urllib.parse import quote

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.config import settings
from app.schemas.oauth_account import (
    OAuthStatusResponse,
    OAuthStatusUpdate,
    YouTubeChannelListResponse,
)
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
    try:
        url = oauth_service.get_youtube_connect_url()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"url": url}


@router.get("/youtube/callback")
def oauth_callback(
    code: str | None = Query(default=None),
    error: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    if error:
        redirect_url = _build_frontend_redirect(success=False, error=error)
        return RedirectResponse(redirect_url)
    if not code:
        raise HTTPException(status_code=400, detail="Missing OAuth code")
    try:
        oauth_service.exchange_youtube_code(db, code)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    redirect_url = _build_frontend_redirect(success=True)
    return RedirectResponse(redirect_url)


@router.get("/youtube/channels", response_model=YouTubeChannelListResponse)
def list_channels(db: Session = Depends(get_db)):
    try:
        items = oauth_service.list_youtube_channels(db)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"items": items}


def _build_frontend_redirect(success: bool, error: str | None = None) -> str:
    base = settings.frontend_url or "http://localhost:3000/setup"
    if "?" in base:
        sep = "&"
    else:
        sep = "?"
    if success:
        return f"{base}{sep}oauth=success"
    if error:
        return f"{base}{sep}oauth=error&message={quote(error)}"
    return f"{base}{sep}oauth=error"

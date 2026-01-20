from datetime import datetime, timezone
from urllib.parse import urlencode

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models.oauth_account import OAuthAccount
from app.services.youtube import YouTubeClient

DEFAULT_OAUTH_ID = "default"
YOUTUBE_SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
YOUTUBE_TOKEN_URI = "https://oauth2.googleapis.com/token"


def get_oauth_account(db: Session) -> OAuthAccount:
    instance = db.get(OAuthAccount, DEFAULT_OAUTH_ID)
    if instance:
        return instance
    instance = OAuthAccount(id=DEFAULT_OAUTH_ID, connected=False, permission_granted=False)
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def update_oauth_account(db: Session, patch: dict) -> OAuthAccount:
    instance = get_oauth_account(db)
    for key, value in patch.items():
        if hasattr(instance, key) and value is not None:
            setattr(instance, key, value)
    db.commit()
    db.refresh(instance)
    return instance


def _ensure_utc_aware(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _ensure_utc_naive(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
        return value
    return value.astimezone(timezone.utc).replace(tzinfo=None)


def _ensure_oauth_config():
    if not settings.youtube_client_id or not settings.youtube_client_secret or not settings.youtube_redirect_uri:
        raise ValueError("YouTube OAuth config missing")


def _build_client_config() -> dict:
    return {
        "web": {
            "client_id": settings.youtube_client_id,
            "client_secret": settings.youtube_client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/v2/auth",
            "token_uri": YOUTUBE_TOKEN_URI,
            "redirect_uris": [settings.youtube_redirect_uri],
        }
    }


def get_youtube_connect_url() -> str:
    _ensure_oauth_config()
    params = {
        "client_id": settings.youtube_client_id,
        "redirect_uri": settings.youtube_redirect_uri,
        "response_type": "code",
        "access_type": "offline",
        "prompt": "consent",
        "include_granted_scopes": "true",
        "scope": " ".join(YOUTUBE_SCOPES),
    }
    return f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"


def exchange_youtube_code(db: Session, code: str) -> OAuthAccount:
    _ensure_oauth_config()
    flow = Flow.from_client_config(
        _build_client_config(),
        scopes=YOUTUBE_SCOPES,
        redirect_uri=settings.youtube_redirect_uri,
    )
    flow.fetch_token(code=code)
    credentials = flow.credentials
    expiry = _ensure_utc_aware(credentials.expiry)
    patch = {
        "connected": True,
        "permission_granted": True,
        "scopes": list(credentials.scopes) if credentials.scopes else list(YOUTUBE_SCOPES),
        "access_token": credentials.token,
        "token_expiry": expiry,
    }
    if credentials.refresh_token:
        patch["refresh_token"] = credentials.refresh_token
    return update_oauth_account(db, patch)


def _build_credentials(db: Session) -> Credentials:
    _ensure_oauth_config()
    account = get_oauth_account(db)
    if not account.access_token:
        raise ValueError("OAuth not connected")
    scopes = account.scopes or list(YOUTUBE_SCOPES)
    creds = Credentials(
        token=account.access_token,
        refresh_token=account.refresh_token,
        token_uri=YOUTUBE_TOKEN_URI,
        client_id=settings.youtube_client_id,
        client_secret=settings.youtube_client_secret,
        scopes=scopes,
    )
    if account.token_expiry:
        creds.expiry = _ensure_utc_naive(account.token_expiry)
    if creds.expired:
        if not creds.refresh_token:
            raise ValueError("OAuth token expired, reconnect required")
        creds.refresh(Request())
        patch = {
            "access_token": creds.token,
            "token_expiry": _ensure_utc_aware(creds.expiry),
        }
        if creds.refresh_token:
            patch["refresh_token"] = creds.refresh_token
        if creds.scopes:
            patch["scopes"] = list(creds.scopes)
        update_oauth_account(db, patch)
    return creds


def list_youtube_channels(db: Session) -> list[dict]:
    creds = _build_credentials(db)
    client = YouTubeClient(credentials=creds)
    response = client.list_channels()
    items = []
    for item in response.get("items", []):
        channel_id = item.get("id")
        if not channel_id:
            continue
        snippet = item.get("snippet", {}) or {}
        stats = item.get("statistics", {}) or {}
        custom_url = snippet.get("customUrl")
        url = None
        if custom_url:
            url = f"https://www.youtube.com/{custom_url}"
        elif channel_id:
            url = f"https://www.youtube.com/channel/{channel_id}"
        thumbnails = snippet.get("thumbnails", {}) or {}
        thumb = thumbnails.get("default", {}) or thumbnails.get("medium", {}) or thumbnails.get("high", {})
        subscriber_count = stats.get("subscriberCount")
        items.append(
            {
                "id": channel_id,
                "name": snippet.get("title"),
                "handle": custom_url,
                "url": url,
                "subscriber_count": int(subscriber_count) if subscriber_count else None,
                "thumbnail_url": thumb.get("url") if isinstance(thumb, dict) else None,
            }
        )
    return items

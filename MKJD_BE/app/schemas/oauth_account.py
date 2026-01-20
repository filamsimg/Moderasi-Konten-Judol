from datetime import datetime
from typing import Optional

from app.schemas.common import APIModel


class OAuthStatusResponse(APIModel):
    connected: bool
    permission_granted: bool
    account_email: Optional[str] = None
    channel_name: Optional[str] = None
    channel_id: Optional[str] = None
    channel_handle: Optional[str] = None
    channel_url: Optional[str] = None
    last_sync: Optional[datetime] = None
    token_expiry: Optional[datetime] = None
    scopes: Optional[list[str]] = None


class OAuthStatusUpdate(APIModel):
    connected: Optional[bool] = None
    permission_granted: Optional[bool] = None
    account_email: Optional[str] = None
    channel_name: Optional[str] = None
    channel_id: Optional[str] = None
    channel_handle: Optional[str] = None
    channel_url: Optional[str] = None
    last_sync: Optional[datetime] = None
    token_expiry: Optional[datetime] = None
    scopes: Optional[list[str]] = None

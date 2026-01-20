from sqlalchemy import Boolean, Column, DateTime, JSON, String, Text
from sqlalchemy.sql import func

from app.db.base import Base


class OAuthAccount(Base):
    __tablename__ = "oauth_accounts"

    id = Column(String(64), primary_key=True)
    account_email = Column(String(255))
    channel_name = Column(String(255))
    channel_id = Column(String(64), index=True)
    channel_handle = Column(String(64))
    channel_url = Column(String(255))
    connected = Column(Boolean, default=False)
    permission_granted = Column(Boolean, default=False)
    scopes = Column(JSON)
    access_token = Column(Text)
    refresh_token = Column(Text)
    token_expiry = Column(DateTime(timezone=True))
    last_sync = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

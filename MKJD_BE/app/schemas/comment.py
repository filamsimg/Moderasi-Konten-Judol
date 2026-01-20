from datetime import datetime
from typing import Optional

from app.schemas.common import APIModel, Decision, YTStatus


class CommentBase(APIModel):
    id: str
    video_id: Optional[str] = None
    video_title: Optional[str] = None
    author_name: Optional[str] = None
    author_channel_id: Optional[str] = None
    text_raw: str
    text_norm: Optional[str] = None
    published_at: Optional[datetime] = None
    fetched_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    score: Optional[float] = None
    decision: Optional[Decision] = None
    yt_status: Optional[YTStatus] = None
    language: Optional[str] = None
    parent_id: Optional[str] = None
    is_reply: Optional[bool] = False


class CommentCreate(APIModel):
    id: str
    video_id: Optional[str] = None
    video_title: Optional[str] = None
    author_name: Optional[str] = None
    author_channel_id: Optional[str] = None
    text_raw: str
    published_at: Optional[datetime] = None
    language: Optional[str] = None
    parent_id: Optional[str] = None
    is_reply: Optional[bool] = False


class CommentResponse(CommentBase):
    pass


class CommentListResponse(APIModel):
    items: list[CommentResponse]
    total: int
    limit: int
    offset: int

from sqlalchemy import Boolean, Column, DateTime, Enum, Float, String, Text
from sqlalchemy.sql import func

from app.db.base import Base
from app.db.models.enums import Decision, YTStatus


class Comment(Base):
    __tablename__ = "comments"

    id = Column(String(64), primary_key=True, index=True)
    video_id = Column(String(64), index=True)
    video_title = Column(String(255))
    author_name = Column(String(255))
    author_channel_id = Column(String(64))
    text_raw = Column(Text, nullable=False)
    text_norm = Column(Text)
    published_at = Column(DateTime(timezone=True))
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    score = Column(Float)
    decision = Column(Enum(Decision, native_enum=False), nullable=True)
    yt_status = Column(Enum(YTStatus, native_enum=False), nullable=True)
    language = Column(String(16))
    parent_id = Column(String(64))
    is_reply = Column(Boolean, default=False)

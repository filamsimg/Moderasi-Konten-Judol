from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, String, Text
from sqlalchemy.sql import func

from app.db.base import Base
from app.db.models.enums import Decision


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String(64), primary_key=True)
    at = Column(DateTime(timezone=True), server_default=func.now())
    action = Column(String(64), nullable=False)
    comment_id = Column(String(64), ForeignKey("comments.id"))
    score = Column(Float)
    from_decision = Column(Enum(Decision, native_enum=False), nullable=True)
    to_decision = Column(Enum(Decision, native_enum=False), nullable=True)
    actor = Column(String(128), nullable=False)
    result = Column(String(32), default="OK")
    note = Column(Text)

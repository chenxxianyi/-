"""Note model."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import String, BigInteger, DateTime, Text, JSON
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.document import Document
    from app.models.annotation import Annotation


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    document_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("documents.id"), nullable=True)
    source_annotation_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("annotations.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    excerpt: Mapped[str | None] = mapped_column(Text, nullable=True)
    source: Mapped[str | None] = mapped_column(String(500), nullable=True)
    content_type: Mapped[str] = mapped_column(String(50), default="richtext", nullable=False)
    tags: Mapped[list | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, onupdate=_utcnow, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # relationships
    user: Mapped["User"] = relationship("User", back_populates="notes")
    document: Mapped["Document | None"] = relationship("Document", back_populates="notes")
    source_annotation_ref: Mapped["Annotation | None"] = relationship("Annotation", back_populates="notes")

    def __repr__(self) -> str:
        return f"<Note id={self.id} title={self.title}>"

"""Annotation model."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, BigInteger, DateTime, Text, JSON
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.document import Document
    from app.models.note import Note


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Annotation(Base):
    __tablename__ = "annotations"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    document_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("documents.id"), nullable=False, index=True)
    page_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    annotation_type: Mapped[str] = mapped_column(String(50), default="highlight", nullable=False)
    color: Mapped[str] = mapped_column(String(50), default="yellow", nullable=False)
    selected_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    position_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    range_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    tags: Mapped[list | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, onupdate=_utcnow, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # relationships
    user: Mapped["User"] = relationship("User", back_populates="annotations")
    document: Mapped["Document"] = relationship("Document", back_populates="annotations")
    notes: Mapped[list["Note"]] = relationship("Note", back_populates="source_annotation_ref")

    def __repr__(self) -> str:
        return f"<Annotation id={self.id} type={self.annotation_type}>"

"""Document repository."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List

from sqlalchemy.orm import Session

from app.models.document import Document


class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, document: Document) -> Document:
        self.db.add(document)
        self.db.flush()
        return document

    def get_by_id_and_user_id(self, document_id: int, user_id: int) -> Document | None:
        return (
            self.db.query(Document)
            .filter(Document.id == document_id, Document.user_id == user_id, Document.deleted_at.is_(None))
            .first()
        )

    def list_by_user(self, user_id: int) -> List[Document]:
        return (
            self.db.query(Document)
            .filter(Document.user_id == user_id, Document.deleted_at.is_(None))
            .order_by(Document.updated_at.desc())
            .all()
        )

    def update(self, document: Document, **kwargs) -> Document:
        for key, value in kwargs.items():
            if hasattr(document, key) and value is not None:
                setattr(document, key, value)
        self.db.flush()
        return document

    def soft_delete(self, document: Document) -> Document:
        document.deleted_at = datetime.now(timezone.utc)
        self.db.flush()
        return document

    def update_read_position(self, document: Document, position: dict | None, progress: int | None = None) -> Document:
        document.last_read_position = position
        document.last_read_at = datetime.now(timezone.utc)
        self.db.flush()
        return document

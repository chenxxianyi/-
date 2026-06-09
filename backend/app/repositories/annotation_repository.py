"""Annotation repository."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List

from sqlalchemy.orm import Session

from app.models.annotation import Annotation


class AnnotationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, annotation: Annotation) -> Annotation:
        self.db.add(annotation)
        self.db.flush()
        return annotation

    def get_by_id_and_user_id(self, annotation_id: int, user_id: int) -> Annotation | None:
        return (
            self.db.query(Annotation)
            .filter(Annotation.id == annotation_id, Annotation.user_id == user_id, Annotation.deleted_at.is_(None))
            .first()
        )

    def list_by_document(self, document_id: int, user_id: int) -> List[Annotation]:
        return (
            self.db.query(Annotation)
            .filter(
                Annotation.document_id == document_id,
                Annotation.user_id == user_id,
                Annotation.deleted_at.is_(None),
            )
            .order_by(Annotation.created_at.desc())
            .all()
        )

    def list_by_user(self, user_id: int, limit: int = 20) -> List[Annotation]:
        return (
            self.db.query(Annotation)
            .filter(Annotation.user_id == user_id, Annotation.deleted_at.is_(None))
            .order_by(Annotation.created_at.desc())
            .limit(limit)
            .all()
        )

    def update(self, annotation: Annotation, **kwargs) -> Annotation:
        for key, value in kwargs.items():
            if hasattr(annotation, key) and value is not None:
                setattr(annotation, key, value)
        self.db.flush()
        return annotation

    def soft_delete(self, annotation: Annotation) -> Annotation:
        annotation.deleted_at = datetime.now(timezone.utc)
        self.db.flush()
        return annotation

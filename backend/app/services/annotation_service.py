"""Annotation service - handles annotation CRUD."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.models.annotation import Annotation
from app.models.user import User
from app.repositories.annotation_repository import AnnotationRepository
from app.repositories.document_repository import DocumentRepository


class AnnotationService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = AnnotationRepository(db)
        self.doc_repo = DocumentRepository(db)

    def _verify_document_ownership(self, user: User, document_id: int) -> None:
        """Verify that the document belongs to the user."""
        doc = self.doc_repo.get_by_id_and_user_id(document_id, user.id)
        if not doc:
            raise NotFoundException("Document not found")

    def create(self, user: User, data: dict) -> Annotation:
        """Create a new annotation."""
        self._verify_document_ownership(user, data["document_id"])

        annotation = Annotation(
            user_id=user.id,
            document_id=data["document_id"],
            page_number=data.get("page_number"),
            annotation_type=data.get("annotation_type", "highlight"),
            color=data.get("color", "yellow"),
            selected_text=data.get("selected_text"),
            note=data.get("note"),
            position_data=data.get("position_data"),
            range_data=data.get("range_data"),
            tags=data.get("tags"),
        )
        created = self.repo.create(annotation)
        self.db.commit()
        self.db.refresh(created)
        return created

    def list_by_document(self, user: User, document_id: int) -> list[Annotation]:
        """List annotations for a document."""
        self._verify_document_ownership(user, document_id)
        return self.repo.list_by_document(document_id, user.id)

    def update(self, user: User, annotation_id: int, data: dict) -> Annotation:
        """Update an annotation."""
        annotation = self.repo.get_by_id_and_user_id(annotation_id, user.id)
        if not annotation:
            raise NotFoundException("Annotation not found")

        updated = self.repo.update(annotation, **data)
        self.db.commit()
        self.db.refresh(updated)
        return updated

    def delete(self, user: User, annotation_id: int) -> None:
        """Soft delete an annotation."""
        annotation = self.repo.get_by_id_and_user_id(annotation_id, user.id)
        if not annotation:
            raise NotFoundException("Annotation not found")

        self.repo.soft_delete(annotation)
        self.db.commit()

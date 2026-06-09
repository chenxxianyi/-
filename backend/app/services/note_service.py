"""Note service - handles note CRUD and creation from annotations."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.models.annotation import Annotation
from app.models.note import Note
from app.models.user import User
from app.repositories.annotation_repository import AnnotationRepository
from app.repositories.document_repository import DocumentRepository
from app.repositories.note_repository import NoteRepository


class NoteService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = NoteRepository(db)
        self.doc_repo = DocumentRepository(db)
        self.annotation_repo = AnnotationRepository(db)

    def _verify_document_ownership(self, user: User, document_id: int) -> None:
        """Verify that the document belongs to the user."""
        doc = self.doc_repo.get_by_id_and_user_id(document_id, user.id)
        if not doc:
            raise NotFoundException("Document not found")

    def create(self, user: User, data: dict) -> Note:
        """Create a new note."""
        if data.get("document_id"):
            self._verify_document_ownership(user, data["document_id"])

        note = Note(
            user_id=user.id,
            document_id=data.get("document_id"),
            source_annotation_id=data.get("source_annotation_id"),
            title=data.get("title", ""),
            content=data.get("content"),
            excerpt=data.get("excerpt"),
            source=data.get("source"),
            content_type=data.get("content_type", "richtext"),
            tags=data.get("tags"),
        )
        created = self.repo.create(note)
        self.db.commit()
        self.db.refresh(created)
        return created

    def list_notes(self, user: User) -> list[Note]:
        """List all notes for a user."""
        return self.repo.list_by_user(user.id)

    def get_note(self, user: User, note_id: int) -> Note:
        """Get a single note by ID."""
        note = self.repo.get_by_id_and_user_id(note_id, user.id)
        if not note:
            raise NotFoundException("Note not found")
        return note

    def update(self, user: User, note_id: int, data: dict) -> Note:
        """Update a note."""
        note = self.get_note(user, note_id)
        updated = self.repo.update(note, **data)
        self.db.commit()
        self.db.refresh(updated)
        return updated

    def delete(self, user: User, note_id: int) -> None:
        """Soft delete a note."""
        note = self.get_note(user, note_id)
        self.repo.soft_delete(note)
        self.db.commit()

    def create_from_annotation(self, user: User, annotation_id: int, document_id: int, title: str | None = None) -> Note:
        """Create a note from an annotation's selected text."""
        # Verify ownership of both document and annotation
        self._verify_document_ownership(user, document_id)
        annotation = self.annotation_repo.get_by_id_and_user_id(annotation_id, user.id)
        if not annotation:
            raise NotFoundException("Annotation not found")

        selected_text = annotation.selected_text or ""
        note_title = title or (selected_text[:18] if selected_text else "新摘录")

        note = Note(
            user_id=user.id,
            document_id=document_id,
            source_annotation_id=annotation_id,
            title=note_title,
            content=f"<p>{selected_text}</p>",
            excerpt=selected_text,
            source=annotation.document.file_name if annotation.document else None,
            content_type="richtext",
            tags=["摘录"] if selected_text else [],
        )
        created = self.repo.create(note)
        self.db.commit()
        self.db.refresh(created)
        return created

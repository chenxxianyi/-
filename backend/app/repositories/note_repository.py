"""Note repository."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List

from sqlalchemy.orm import Session

from app.models.note import Note


class NoteRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, note: Note) -> Note:
        self.db.add(note)
        self.db.flush()
        return note

    def get_by_id_and_user_id(self, note_id: int, user_id: int) -> Note | None:
        return (
            self.db.query(Note)
            .filter(Note.id == note_id, Note.user_id == user_id, Note.deleted_at.is_(None))
            .first()
        )

    def list_by_user(self, user_id: int) -> List[Note]:
        return (
            self.db.query(Note)
            .filter(Note.user_id == user_id, Note.deleted_at.is_(None))
            .order_by(Note.updated_at.desc())
            .all()
        )

    def update(self, note: Note, **kwargs) -> Note:
        for key, value in kwargs.items():
            if hasattr(note, key) and value is not None:
                setattr(note, key, value)
        self.db.flush()
        return note

    def soft_delete(self, note: Note) -> Note:
        note.deleted_at = datetime.now(timezone.utc)
        self.db.flush()
        return note

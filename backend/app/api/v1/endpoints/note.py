"""Note endpoints - CRUD and create from annotation."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.exceptions import AppException
from app.db.session import get_db
from app.models.user import User
from app.schemas.note import NoteCreate, NoteFromAnnotation, NoteRead, NoteUpdate
from app.services.note_service import NoteService
from app.utils.response import fail, success

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("")
def list_notes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all notes for the current user."""
    try:
        service = NoteService(db)
        notes = service.list_notes(current_user)
        result = [NoteRead.model_validate(n).model_dump(by_alias=True) for n in notes]
        return success(data=result)
    except AppException as e:
        return fail(code=e.code, message=e.message)


@router.post("")
def create_note(
    payload: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new note."""
    try:
        service = NoteService(db)
        data = payload.model_dump(by_alias=True)
        note = service.create(current_user, data)
        result = NoteRead.model_validate(note).model_dump(by_alias=True)
        return success(data=result)
    except AppException as e:
        return fail(code=e.code, message=e.message)


@router.post("/from-annotation")
def create_note_from_annotation(
    payload: NoteFromAnnotation,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a note from an annotation."""
    try:
        service = NoteService(db)
        note = service.create_from_annotation(
            user=current_user,
            annotation_id=payload.sourceAnnotationId,
            document_id=payload.documentId,
            title=payload.title,
        )
        result = NoteRead.model_validate(note).model_dump(by_alias=True)
        return success(data=result)
    except AppException as e:
        return fail(code=e.code, message=e.message)


@router.get("/{note_id}")
def get_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a single note."""
    try:
        service = NoteService(db)
        note = service.get_note(current_user, note_id)
        result = NoteRead.model_validate(note).model_dump(by_alias=True)
        return success(data=result)
    except AppException as e:
        return fail(code=e.code, message=e.message)


@router.put("/{note_id}")
def update_note(
    note_id: int,
    payload: NoteUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a note."""
    try:
        service = NoteService(db)
        data = payload.model_dump(exclude_none=True, by_alias=True)
        note = service.update(current_user, note_id, data)
        result = NoteRead.model_validate(note).model_dump(by_alias=True)
        return success(data=result)
    except AppException as e:
        return fail(code=e.code, message=e.message)


@router.delete("/{note_id}")
def delete_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Soft delete a note."""
    try:
        service = NoteService(db)
        service.delete(current_user, note_id)
        return success(message="Note deleted")
    except AppException as e:
        return fail(code=e.code, message=e.message)

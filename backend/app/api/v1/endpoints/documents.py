"""Document endpoints - CRUD, upload, content, read position."""

from __future__ import annotations

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.exceptions import AppException
from app.db.session import get_db
from app.models.user import User
from app.schemas.document import DocumentRead, DocumentUpdate, ReadPositionUpdate
from app.services.document_service import DocumentService
from app.utils.response import fail, success

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("")
def list_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all documents for the current user."""
    service = DocumentService(db)
    docs = service.list_documents(current_user)

    result = []
    for doc in docs:
        d = DocumentRead.model_validate(doc)
        d.displaySize = service.to_display_size(doc.file_size)
        d.annotationCount = len(doc.annotations) if doc.annotations else 0
        d.progress = 0  # TODO: calculate from read position
        if doc.last_read_at:
            d.lastReadAt = doc.last_read_at.isoformat()
        d.uploadedAt = doc.created_at.isoformat()
        d.createdAt = doc.created_at.isoformat()
        d.updatedAt = doc.updated_at.isoformat()
        result.append(d)

    return success(data=[r.model_dump() for r in result])


@router.get("/{document_id}")
def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get document details."""
    try:
        service = DocumentService(db)
        doc = service.get_document(current_user, document_id)
        d = DocumentRead.model_validate(doc)
        d.displaySize = service.to_display_size(doc.file_size)
        d.annotationCount = len(doc.annotations) if doc.annotations else 0
        if doc.last_read_at:
            d.lastReadAt = doc.last_read_at.isoformat()
        d.uploadedAt = doc.created_at.isoformat()
        d.createdAt = doc.created_at.isoformat()
        d.updatedAt = doc.updated_at.isoformat()
        return success(data=d.model_dump())
    except AppException as e:
        return fail(code=e.code, message=e.message)


@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload a document file."""
    try:
        service = DocumentService(db)
        file_data = file.file.read()
        doc = service.upload(current_user, file.filename or "untitled", file_data)

        d = DocumentRead.model_validate(doc)
        d.displaySize = service.to_display_size(doc.file_size)
        d.uploadedAt = doc.created_at.isoformat()
        d.createdAt = doc.created_at.isoformat()
        d.updatedAt = doc.updated_at.isoformat()
        return success(data=d.model_dump())
    except AppException as e:
        return fail(code=e.code, message=e.message)


@router.put("/{document_id}")
def update_document(
    document_id: int,
    payload: DocumentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update document metadata (rename)."""
    try:
        service = DocumentService(db)
        doc = service.update_document(current_user, document_id, title=payload.title)
        d = DocumentRead.model_validate(doc)
        return success(data=d.model_dump())
    except AppException as e:
        return fail(code=e.code, message=e.message)


@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Soft delete a document."""
    try:
        service = DocumentService(db)
        service.delete_document(current_user, document_id)
        return success(message="Document deleted")
    except AppException as e:
        return fail(code=e.code, message=e.message)


@router.get("/{document_id}/content")
def get_document_content(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get parsed document content."""
    try:
        service = DocumentService(db)
        content, content_type = service.get_document_content(current_user, document_id)
        return success(data={"id": document_id, "content": content, "contentType": content_type})
    except AppException as e:
        return fail(code=e.code, message=e.message)


@router.put("/{document_id}/read-position")
def save_read_position(
    document_id: int,
    payload: ReadPositionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Save reading position/progress."""
    try:
        service = DocumentService(db)
        doc = service.save_read_position(current_user, document_id, payload.position, payload.progress)
        return success(data={"id": doc.id, "progress": payload.progress})
    except AppException as e:
        return fail(code=e.code, message=e.message)

"""Annotation endpoints - CRUD."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.exceptions import AppException
from app.db.session import get_db
from app.models.user import User
from app.schemas.annotation import AnnotationCreate, AnnotationRead, AnnotationUpdate
from app.services.annotation_service import AnnotationService
from app.utils.response import fail, success

router = APIRouter(prefix="/documents/{document_id}/annotations", tags=["annotations"])


@router.get("")
def list_annotations(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List annotations for a document."""
    try:
        service = AnnotationService(db)
        annotations = service.list_by_document(current_user, document_id)
        result = [AnnotationRead.model_validate(a).model_dump(by_alias=True) for a in annotations]
        return success(data=result)
    except AppException as e:
        return fail(code=e.code, message=e.message)


@router.post("")
def create_annotation(
    document_id: int,
    payload: AnnotationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new annotation."""
    try:
        service = AnnotationService(db)
        data = payload.model_dump(by_alias=True)
        data["document_id"] = document_id
        annotation = service.create(current_user, data)
        result = AnnotationRead.model_validate(annotation).model_dump(by_alias=True)
        return success(data=result)
    except AppException as e:
        return fail(code=e.code, message=e.message)


@router.get("/{annotation_id}")
def get_annotation(
    document_id: int,
    annotation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a single annotation."""
    try:
        service = AnnotationService(db)
        annotations = service.list_by_document(current_user, document_id)
        annotation = next((a for a in annotations if a.id == annotation_id), None)
        if not annotation:
            return fail(code=404, message="Annotation not found")
        result = AnnotationRead.model_validate(annotation).model_dump(by_alias=True)
        return success(data=result)
    except AppException as e:
        return fail(code=e.code, message=e.message)


@router.put("/{annotation_id}")
def update_annotation(
    document_id: int,
    annotation_id: int,
    payload: AnnotationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update an annotation."""
    try:
        service = AnnotationService(db)
        data = payload.model_dump(exclude_none=True, by_alias=True)
        annotation = service.update(current_user, annotation_id, data)
        result = AnnotationRead.model_validate(annotation).model_dump(by_alias=True)
        return success(data=result)
    except AppException as e:
        return fail(code=e.code, message=e.message)


@router.delete("/{annotation_id}")
def delete_annotation(
    document_id: int,
    annotation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Soft delete an annotation."""
    try:
        service = AnnotationService(db)
        service.delete(current_user, annotation_id)
        return success(message="Annotation deleted")
    except AppException as e:
        return fail(code=e.code, message=e.message)


# Also expose flat annotation endpoints for convenience
flat_router = APIRouter(prefix="/annotations", tags=["annotations"])


@flat_router.get("")
def list_all_annotations(
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List recent annotations for the current user."""
    try:
        from app.repositories.annotation_repository import AnnotationRepository
        repo = AnnotationRepository(db)
        annotations = repo.list_by_user(current_user.id, limit=limit)
        result = [AnnotationRead.model_validate(a).model_dump(by_alias=True) for a in annotations]
        return success(data=result)
    except AppException as e:
        return fail(code=e.code, message=e.message)


@flat_router.get("/{annotation_id}")
def get_annotation_flat(
    annotation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a single annotation by ID."""
    try:
        service = AnnotationService(db)
        # We need to find it - use the repo directly
        from app.repositories.annotation_repository import AnnotationRepository
        repo = AnnotationRepository(db)
        annotation = repo.get_by_id_and_user_id(annotation_id, current_user.id)
        if not annotation:
            return fail(code=404, message="Annotation not found")
        result = AnnotationRead.model_validate(annotation).model_dump(by_alias=True)
        return success(data=result)
    except AppException as e:
        return fail(code=e.code, message=e.message)


@flat_router.put("/{annotation_id}")
def update_annotation_flat(
    annotation_id: int,
    payload: AnnotationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update an annotation by ID."""
    try:
        service = AnnotationService(db)
        data = payload.model_dump(exclude_none=True, by_alias=True)
        annotation = service.update(current_user, annotation_id, data)
        result = AnnotationRead.model_validate(annotation).model_dump(by_alias=True)
        return success(data=result)
    except AppException as e:
        return fail(code=e.code, message=e.message)


@flat_router.delete("/{annotation_id}")
def delete_annotation_flat(
    annotation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete an annotation by ID."""
    try:
        service = AnnotationService(db)
        service.delete(current_user, annotation_id)
        return success(message="Annotation deleted")
    except AppException as e:
        return fail(code=e.code, message=e.message)

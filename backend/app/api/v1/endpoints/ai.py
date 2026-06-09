"""AI endpoints - AI reading assistant mock APIs."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.exceptions import AppException
from app.db.session import get_db
from app.models.user import User
from app.schemas.ai import (
    AiAskRequest,
    AiChatRequest,
    AiExplainRequest,
    AiResponse,
    AiSummaryRequest,
    AiTranslateRequest,
)
from app.services.ai_service import AIService
from app.utils.response import fail, success

router = APIRouter(prefix="/documents/{document_id}/ai", tags=["ai"])
flat_router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/ask")
def ask_document(
    document_id: int,
    payload: AiAskRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Ask a question about a document (chat with AI)."""
    try:
        service = AIService(db)
        answer = service.ask(
            user_id=current_user.id,
            document_id=document_id,
            question=payload.question,
        )
        return success(data={"answer": answer})
    except AppException as e:
        return fail(code=e.code, message=e.message)


@flat_router.post("/summary")
def ai_summary(
    payload: AiSummaryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Generate AI summary for a document."""
    try:
        service = AIService(db)
        answer = service.summarize(
            user_id=current_user.id,
            document_id=payload.documentId,
        )
        return success(data={"answer": answer})
    except AppException as e:
        return fail(code=e.code, message=e.message)


@flat_router.post("/explain")
def ai_explain(
    payload: AiExplainRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Explain a selected text from a document."""
    try:
        service = AIService(db)
        answer = service.explain(
            user_id=current_user.id,
            document_id=payload.documentId,
            text=payload.text,
        )
        return success(data={"answer": answer})
    except AppException as e:
        return fail(code=e.code, message=e.message)


@flat_router.post("/translate")
def ai_translate(
    payload: AiTranslateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Translate a selected text from a document."""
    try:
        service = AIService(db)
        answer = service.translate(
            user_id=current_user.id,
            document_id=payload.documentId,
            text=payload.text,
            target_language=payload.targetLanguage,
        )
        return success(data={"answer": answer})
    except AppException as e:
        return fail(code=e.code, message=e.message)


@flat_router.post("/chat")
def ai_chat(
    payload: AiChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Chat with AI about a document."""
    try:
        service = AIService(db)
        answer = service.chat(
            user_id=current_user.id,
            document_id=payload.documentId,
            message=payload.message,
        )
        return success(data={"answer": answer})
    except AppException as e:
        return fail(code=e.code, message=e.message)

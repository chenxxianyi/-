"""AI schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class AiAskRequest(BaseModel):
    question: str = Field(..., min_length=1)


class AiSummaryRequest(BaseModel):
    documentId: int = Field(alias="document_id")
    maxLength: int | None = Field(default=None, alias="max_length")

    model_config = {"populate_by_name": True}


class AiExplainRequest(BaseModel):
    documentId: int = Field(alias="document_id")
    text: str = Field(..., min_length=1)

    model_config = {"populate_by_name": True}


class AiTranslateRequest(BaseModel):
    documentId: int = Field(alias="document_id")
    text: str = Field(..., min_length=1)
    targetLanguage: str = Field(default="中文", alias="target_language")

    model_config = {"populate_by_name": True}


class AiChatRequest(BaseModel):
    documentId: int = Field(alias="document_id")
    message: str = Field(..., min_length=1)

    model_config = {"populate_by_name": True}


class AiResponse(BaseModel):
    answer: str

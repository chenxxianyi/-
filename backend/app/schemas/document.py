"""Document schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class DocumentRead(BaseModel):
    id: int
    title: str
    fileName: str = Field(alias="file_name")
    fileType: str = Field(alias="file_type")
    mimeType: str = Field(alias="mime_type")
    fileSize: int = Field(alias="file_size")
    displaySize: str = ""
    parsedStatus: str = Field(default="pending", alias="parsed_status")
    pageCount: int = Field(default=0, alias="page_count")
    wordCount: int = Field(default=0, alias="word_count")
    annotationCount: int = 0
    progress: int = 0
    lastReadPosition: dict | None = Field(default=None, alias="last_read_position")
    lastReadAt: str | None = Field(default=None, alias="last_read_at")
    uploadedAt: str = Field(alias="created_at")
    createdAt: str = Field(alias="created_at")
    updatedAt: str = Field(alias="updated_at")

    model_config = {"from_attributes": True, "populate_by_name": True}


class DocumentUpdate(BaseModel):
    title: str | None = None


class ReadPositionUpdate(BaseModel):
    position: dict | None = None
    progress: int | None = None


class DocumentContent(BaseModel):
    id: int
    content: str
    contentType: str = "text"

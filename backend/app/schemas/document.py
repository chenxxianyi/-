"""Document schemas."""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


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
    lastReadPosition: Optional[dict] = Field(default=None, alias="last_read_position")
    lastReadAt: Optional[str] = Field(default=None, alias="last_read_at")
    uploadedAt: str = Field(default="", alias="created_at")
    createdAt: str = Field(default="", alias="created_at")
    updatedAt: str = Field(default="", alias="updated_at")

    model_config = {"from_attributes": True, "populate_by_name": True}

    @field_validator("uploadedAt", "createdAt", "updatedAt", "lastReadAt", mode="before")
    @classmethod
    def coerce_datetime(cls, v: Any) -> str:
        if v is None:
            return ""
        if isinstance(v, str):
            return v
        if isinstance(v, datetime):
            return v.isoformat()
        return str(v)


class DocumentUpdate(BaseModel):
    title: Optional[str] = None


class ReadPositionUpdate(BaseModel):
    position: Optional[dict] = None
    progress: Optional[int] = None


class DocumentContent(BaseModel):
    id: int
    content: str
    contentType: str = "text"

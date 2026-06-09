"""Note schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    documentId: int | None = Field(default=None, alias="document_id")
    sourceAnnotationId: int | None = Field(default=None, alias="source_annotation_id")
    title: str = ""
    content: str | None = None
    excerpt: str | None = None
    source: str | None = None
    contentType: str = Field(default="richtext", alias="content_type")
    tags: list[str] | None = None

    model_config = {"populate_by_name": True}


class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    excerpt: str | None = None
    source: str | None = None
    contentType: str | None = Field(default=None, alias="content_type")
    tags: list[str] | None = None

    model_config = {"populate_by_name": True}


class NoteFromAnnotation(BaseModel):
    documentId: int = Field(alias="document_id")
    sourceAnnotationId: int = Field(alias="source_annotation_id")
    title: str | None = None

    model_config = {"populate_by_name": True}


class NoteRead(BaseModel):
    id: int
    documentId: int | None = Field(default=None, alias="document_id")
    sourceAnnotationId: int | None = Field(default=None, alias="source_annotation_id")
    title: str
    content: str | None = None
    excerpt: str | None = None
    source: str | None = None
    contentType: str = Field(alias="content_type")
    tags: list[str] | None = None
    createdAt: str = Field(alias="created_at")
    updatedAt: str = Field(alias="updated_at")

    model_config = {"from_attributes": True, "populate_by_name": True}

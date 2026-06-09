"""Annotation schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class AnnotationCreate(BaseModel):
    documentId: int = Field(alias="document_id")
    pageNumber: int | None = Field(default=None, alias="page_number")
    annotationType: str = Field(default="highlight", alias="annotation_type")
    color: str = "yellow"
    selectedText: str | None = Field(default=None, alias="selected_text")
    note: str | None = None
    positionData: dict | None = Field(default=None, alias="position_data")
    rangeData: dict | None = Field(default=None, alias="range_data")
    tags: list[str] | None = None

    model_config = {"populate_by_name": True}


class AnnotationUpdate(BaseModel):
    annotationType: str | None = Field(default=None, alias="annotation_type")
    color: str | None = None
    selectedText: str | None = Field(default=None, alias="selected_text")
    note: str | None = None
    positionData: dict | None = Field(default=None, alias="position_data")
    rangeData: dict | None = Field(default=None, alias="range_data")
    tags: list[str] | None = None

    model_config = {"populate_by_name": True}


class AnnotationRead(BaseModel):
    id: int
    documentId: int = Field(alias="document_id")
    pageNumber: int | None = Field(default=None, alias="page_number")
    annotationType: str = Field(alias="annotation_type")
    color: str
    selectedText: str | None = Field(default=None, alias="selected_text")
    note: str | None = None
    positionData: dict | None = Field(default=None, alias="position_data")
    rangeData: dict | None = Field(default=None, alias="range_data")
    tags: list[str] | None = None
    createdAt: str = Field(alias="created_at")
    updatedAt: str = Field(alias="updated_at")

    model_config = {"from_attributes": True, "populate_by_name": True}

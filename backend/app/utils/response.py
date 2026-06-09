"""Unified response utility."""

from __future__ import annotations

from typing import Any

from app.schemas.common import ApiResponse


def success(data: Any = None, message: str = "success") -> ApiResponse:
    """Return a success response."""
    return ApiResponse.success(data=data, message=message)


def fail(code: int = 400, message: str = "Bad Request") -> ApiResponse:
    """Return a failure response."""
    return ApiResponse.fail(code=code, message=message)

"""Common schemas - unified response wrapper."""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """Unified API response wrapper that matches frontend ApiResponse interface."""

    code: int = 0
    message: str = "success"
    data: T | None = None

    @classmethod
    def success(cls, data: Any = None, message: str = "success") -> "ApiResponse":
        return cls(code=0, message=message, data=data)

    @classmethod
    def fail(cls, code: int = 400, message: str = "Bad Request") -> "ApiResponse":
        return cls(code=code, message=message, data=None)

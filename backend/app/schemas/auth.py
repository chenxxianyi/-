"""Auth schemas."""

from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., max_length=255)
    password: str = Field(..., min_length=6, max_length=128)


class LoginRequest(BaseModel):
    email: str = Field(..., max_length=255)
    password: str = Field(..., max_length=128)


class LoginResponse(BaseModel):
    accessToken: str
    tokenType: str = "bearer"


class UserRead(BaseModel):
    id: int
    username: str
    email: str

    model_config = {"from_attributes": True}

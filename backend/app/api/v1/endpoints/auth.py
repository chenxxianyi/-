"""Auth endpoints - login, register, get current user."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse, RegisterRequest, UserRead
from app.services.auth_service import AuthService
from app.utils.response import success, fail

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user."""
    try:
        service = AuthService(db)
        result = service.register(
            username=payload.username,
            email=payload.email,
            password=payload.password,
        )
        return success(data=result)
    except Exception as e:
        return fail(code=409, message=str(e))


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """Login and get access token."""
    try:
        service = AuthService(db)
        result = service.login(email=payload.email, password=payload.password)
        return success(data=result)
    except Exception as e:
        return fail(code=401, message=str(e))


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    """Get current user profile."""
    return success(data=UserRead.model_validate(current_user))

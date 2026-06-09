"""User endpoints - user profile."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.auth import UserRead
from app.utils.response import success

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def get_profile(current_user: User = Depends(get_current_user)):
    """Get the current user's profile."""
    return success(data=UserRead.model_validate(current_user))

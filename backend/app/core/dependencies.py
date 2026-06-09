"""Security dependency: get current user from JWT token."""

from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.exceptions import UnauthorizedException
from app.db.session import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.utils.jwt import verify_token

security_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Extract and validate the current user from the JWT token."""
    if credentials is None:
        raise UnauthorizedException("Missing authorization token")

    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise UnauthorizedException("Invalid or expired token")

    subject = payload.get("sub")
    if subject is None:
        raise UnauthorizedException("Invalid token payload")
    try:
        user_id = int(subject)
    except (TypeError, ValueError):
        raise UnauthorizedException("Invalid token payload") from None

    repo = UserRepository(db)
    user = repo.get_by_id(user_id)
    if user is None:
        raise UnauthorizedException("User not found")

    return user


def get_optional_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security_scheme),
    db: Session = Depends(get_db),
) -> User | None:
    """Try to get the current user, return None if not authenticated."""
    if credentials is None:
        return None
    try:
        return get_current_user(credentials, db)
    except UnauthorizedException:
        return None

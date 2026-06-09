"""User service - handles user profile operations."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)

    def get_profile(self, user: User) -> User:
        """Get the current user's profile."""
        return user

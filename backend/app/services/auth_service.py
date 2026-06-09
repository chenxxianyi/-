"""Auth service - handles registration and login."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.exceptions import ConflictException, UnauthorizedException
from app.repositories.user_repository import UserRepository
from app.utils.jwt import create_access_token
from app.utils.password import hash_password, verify_password


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)

    def register(self, username: str, email: str, password: str) -> dict:
        """Register a new user and return an access token."""
        existing = self.repo.get_by_email(email)
        if existing:
            raise ConflictException("Email already registered")

        password_hash = hash_password(password)
        user = self.repo.create(username=username, email=email, password_hash=password_hash)
        self.db.commit()

        access_token = create_access_token(data={"sub": user.id})
        return {"accessToken": access_token, "tokenType": "bearer"}

    def login(self, email: str, password: str) -> dict:
        """Authenticate a user and return an access token."""
        user = self.repo.get_by_email(email)
        if not user:
            raise UnauthorizedException("Invalid email or password")

        if not verify_password(password, user.password_hash):
            raise UnauthorizedException("Invalid email or password")

        access_token = create_access_token(data={"sub": user.id})
        return {"accessToken": access_token, "tokenType": "bearer"}

"""Main API router that aggregates all endpoint routers."""

from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, documents, annotations, note, ai
from app.core.config import settings

router = APIRouter(prefix=settings.API_PREFIX)

# Auth and users
router.include_router(auth.router)
router.include_router(users.router)

# Documents
router.include_router(documents.router)

# Annotations (both nested under documents and flat)
router.include_router(annotations.router)
router.include_router(annotations.flat_router)

# Notes
router.include_router(note.router)

# AI
router.include_router(ai.router)
router.include_router(ai.flat_router)

"""File utility helpers."""

from __future__ import annotations

import os
import uuid
from pathlib import Path


def generate_storage_path(user_id: int, original_filename: str) -> str:
    """Generate a unique storage path for an uploaded file."""
    ext = Path(original_filename).suffix.lower()
    unique_name = f"{uuid.uuid4().hex}{ext}"
    return f"users/{user_id}/{unique_name}"


def human_readable_size(size_bytes: int) -> str:
    """Convert bytes to a human-readable size string."""
    if size_bytes == 0:
        return "0 B"
    units = ["B", "KB", "MB", "GB"]
    i = 0
    size = float(size_bytes)
    while size >= 1024 and i < len(units) - 1:
        size /= 1024
        i += 1
    return f"{size:.1f} {units[i]}" if i > 0 else f"{int(size)} B"

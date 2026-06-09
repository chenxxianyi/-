"""MIME type detection utility."""

from __future__ import annotations

from pathlib import Path

# Mapping of file extensions to MIME types
MIME_MAP: dict[str, str] = {
    ".pdf": "application/pdf",
    ".md": "text/markdown",
    ".txt": "text/plain",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".bmp": "image/bmp",
    ".webp": "image/webp",
    ".csv": "text/csv",
    ".html": "text/html",
    ".htm": "text/html",
    ".json": "application/json",
    ".xml": "application/xml",
    ".yaml": "text/yaml",
    ".yml": "text/yaml",
    ".epub": "application/epub+zip",
}

SUPPORTED_EXTENSIONS: set[str] = {".pdf", ".md", ".txt", ".docx", ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}
SUPPORTED_DOCUMENT_EXTENSIONS: set[str] = {".pdf", ".md", ".txt", ".docx"}


def get_mime_type(filename: str) -> str:
    """Detect MIME type from filename."""
    ext = Path(filename).suffix.lower()
    return MIME_MAP.get(ext, "application/octet-stream")


def is_supported(filename: str) -> bool:
    """Check if the file extension is supported."""
    ext = Path(filename).suffix.lower()
    return ext in SUPPORTED_EXTENSIONS


def is_document(filename: str) -> bool:
    """Check if the file is a parsable document (not image)."""
    ext = Path(filename).suffix.lower()
    return ext in SUPPORTED_DOCUMENT_EXTENSIONS


def get_file_type(filename: str) -> str:
    """Get the short file type identifier."""
    ext = Path(filename).suffix.lower().lstrip(".")
    return ext if ext else "unknown"

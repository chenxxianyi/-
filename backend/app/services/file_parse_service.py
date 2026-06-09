"""File parsing service - handles document content extraction."""

from __future__ import annotations

import io
import os
import tempfile
from pathlib import Path

import charset_normalizer
import docx
import mammoth
import pypdf


class FileParseService:
    """Extract text content from uploaded documents."""

    @staticmethod
    def parse_content(file_data: bytes, file_name: str) -> tuple[str, str]:
        """
        Parse document content and return (text_content, content_type).

        content_type is one of: 'text', 'markdown', 'html'
        """
        ext = Path(file_name).suffix.lower()

        if ext == ".pdf":
            return FileParseService._parse_pdf(file_data), "text"
        elif ext == ".docx":
            return FileParseService._parse_docx(file_data), "html"
        elif ext == ".md":
            content = FileParseService._parse_text(file_data)
            return content, "markdown"
        elif ext == ".txt":
            return FileParseService._parse_text(file_data), "text"
        else:
            return "", "text"

    @staticmethod
    def _parse_pdf(data: bytes) -> str:
        """Extract text from PDF."""
        text_parts = []
        try:
            reader = pypdf.PdfReader(io.BytesIO(data))
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        except Exception:
            text_parts.append("[PDF parsing encountered an error]")
        return "\n\n".join(text_parts)

    @staticmethod
    def _parse_docx(data: bytes) -> str:
        """Convert DOCX to HTML using mammoth."""
        try:
            result = mammoth.convert_to_html(io.BytesIO(data))
            return result.value
        except Exception:
            try:
                doc = docx.Document(io.BytesIO(data))
                paragraphs = [p.text for p in doc.paragraphs if p.text]
                return "\n\n".join(paragraphs)
            except Exception:
                return "[DOCX parsing encountered an error]"

    @staticmethod
    def _parse_text(data: bytes) -> str:
        """Parse text file with charset detection."""
        try:
            result = charset_normalizer.from_bytes(data)
            return str(result.best())
        except Exception:
            return data.decode("utf-8", errors="replace")

    @staticmethod
    def get_page_count(file_data: bytes, file_name: str) -> int:
        """Estimate page count for the document."""
        ext = Path(file_name).suffix.lower()
        if ext == ".pdf":
            try:
                reader = pypdf.PdfReader(io.BytesIO(file_data))
                return len(reader.pages)
            except Exception:
                return 0
        return 1

    @staticmethod
    def get_word_count(file_data: bytes) -> int:
        """Count words in the file data."""
        try:
            text = FileParseService._parse_text(file_data)
            return len(text.split())
        except Exception:
            return 0

"""Document service - handles document CRUD, upload, and file operations."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException, ValidationException
from app.models.document import Document
from app.models.user import User
from app.repositories.document_repository import DocumentRepository
from app.services.file_parse_service import FileParseService
from app.services.storage_service import StorageService
from app.utils.file import generate_storage_path, human_readable_size
from app.utils.mime import get_file_type, get_mime_type, is_supported


class DocumentService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = DocumentRepository(db)
        self.storage = StorageService()

    def upload(self, user: User, file_name: str, file_data: bytes) -> Document:
        """Upload a document file, store it, and create a document record."""
        if not is_supported(file_name):
            raise ValidationException(f"Unsupported file type: {file_name}")

        mime_type = get_mime_type(file_name)
        file_type = get_file_type(file_name)

        # Store file in MinIO
        storage_path = generate_storage_path(user.id, file_name)
        self.storage.upload(storage_path, file_data, mime_type)

        # Parse content
        parsed_content, content_type = FileParseService.parse_content(file_data, file_name)
        page_count = FileParseService.get_page_count(file_data, file_name)
        word_count = FileParseService.get_word_count(file_data)

        document = Document(
            user_id=user.id,
            title=file_name,
            file_name=file_name,
            file_type=file_type,
            mime_type=mime_type,
            file_size=len(file_data),
            storage_path=storage_path,
            parsed_status="success",
            parsed_content=parsed_content,
            page_count=page_count,
            word_count=word_count,
        )
        created = self.repo.create(document)
        self.db.commit()
        self.db.refresh(created)
        return created

    def list_documents(self, user: User) -> list[Document]:
        """List all documents for a user."""
        return self.repo.list_by_user(user.id)

    def get_document(self, user: User, document_id: int) -> Document:
        """Get a single document by ID, with ownership check."""
        document = self.repo.get_by_id_and_user_id(document_id, user.id)
        if not document:
            raise NotFoundException("Document not found")
        return document

    def get_document_content(self, user: User, document_id: int) -> tuple[str, str]:
        """Get parsed content of a document."""
        document = self.get_document(user, document_id)
        return document.parsed_content or "", document.file_type

    def update_document(self, user: User, document_id: int, title: str | None = None) -> Document:
        """Update document metadata (e.g., rename)."""
        document = self.get_document(user, document_id)
        if title:
            document = self.repo.update(document, title=title, file_name=title)
            self.db.commit()
            self.db.refresh(document)
        return document

    def delete_document(self, user: User, document_id: int) -> None:
        """Soft delete a document."""
        document = self.get_document(user, document_id)
        self.repo.soft_delete(document)
        self.db.commit()

    def save_read_position(self, user: User, document_id: int, position: dict | None, progress: int | None = None) -> Document:
        """Save reading position for a document."""
        document = self.get_document(user, document_id)
        document = self.repo.update_read_position(document, position, progress)
        self.db.commit()
        self.db.refresh(document)
        return document

    def get_preview_url(self, user: User, document_id: int) -> str | None:
        """Get a presigned URL for file preview."""
        document = self.get_document(user, document_id)
        if document.storage_path:
            return self.storage.get_presigned_url(document.storage_path)
        return None

    @staticmethod
    def to_display_size(file_size: int) -> str:
        """Convert file size to human-readable string."""
        return human_readable_size(file_size)

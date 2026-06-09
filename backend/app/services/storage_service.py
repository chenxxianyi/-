"""Storage service - MinIO operations."""

from __future__ import annotations

import io
from typing import Optional

from minio import Minio
from minio.error import S3Error

from app.core.config import settings


class StorageService:
    """Handle file storage operations with MinIO."""

    def __init__(self):
        self.client = Minio(**settings.MINIO_CLIENT_CONFIG)
        self._ensure_bucket()

    def _ensure_bucket(self) -> None:
        """Create the bucket if it doesn't exist."""
        try:
            if not self.client.bucket_exists(settings.MINIO_BUCKET):
                self.client.make_bucket(settings.MINIO_BUCKET)
        except S3Error as e:
            # In development, MinIO might not be available
            if settings.ENV == "development":
                return
            raise

    def upload(self, object_name: str, data: bytes, content_type: str) -> str:
        """Upload a file to MinIO and return the object path."""
        try:
            self.client.put_object(
                bucket_name=settings.MINIO_BUCKET,
                object_name=object_name,
                data=io.BytesIO(data),
                length=len(data),
                content_type=content_type,
            )
            return object_name
        except S3Error as e:
            if settings.ENV == "development":
                # In development without MinIO, still return the path
                return object_name
            raise

    def get_presigned_url(self, object_name: str, expires: int = 3600) -> Optional[str]:
        """Get a presigned URL for temporary access to a file."""
        try:
            return self.client.presigned_get_object(
                bucket_name=settings.MINIO_BUCKET,
                object_name=object_name,
                expires=expires,
            )
        except S3Error:
            if settings.ENV == "development":
                return None
            raise

    def remove(self, object_name: str) -> None:
        """Remove a file from MinIO."""
        try:
            self.client.remove_object(
                bucket_name=settings.MINIO_BUCKET,
                object_name=object_name,
            )
        except S3Error:
            if settings.ENV == "development":
                return
            raise

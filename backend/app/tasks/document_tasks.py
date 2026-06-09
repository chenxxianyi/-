"""Celery tasks for document processing (MVP placeholder)."""

from __future__ import annotations

from app.tasks.celery_app import celery_app


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def parse_document_task(self, document_id: int) -> dict:
    """Parse document content asynchronously.

    MVP: placeholder - actual parsing happens synchronously during upload.
    This task is reserved for future async processing.
    """
    return {"document_id": document_id, "status": "pending"}


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def generate_document_summary_task(self, document_id: int) -> dict:
    """Generate AI summary for a document asynchronously.

    MVP: placeholder for future implementation.
    """
    return {"document_id": document_id, "status": "pending"}


@celery_app.task
def cleanup_deleted_files_task() -> dict:
    """Clean up orphaned files from MinIO.

    MVP: placeholder for future implementation.
    """
    return {"status": "pending"}

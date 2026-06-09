"""Tests for document endpoints."""

from __future__ import annotations

import io

from fastapi.testclient import TestClient


def test_list_documents_empty(test_client: TestClient, auth_headers: dict):
    """Test listing documents when none exist."""
    response = test_client.get("/api/documents", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["data"] == []


def test_upload_document(test_client: TestClient, auth_headers: dict):
    """Test uploading a text file."""
    file_content = b"Hello, this is a test document."
    response = test_client.post(
        "/api/documents/upload",
        headers=auth_headers,
        files={"file": ("test.txt", io.BytesIO(file_content), "text/plain")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["data"]["fileName"] == "test.txt"
    assert data["data"]["fileType"] == "txt"


def test_list_documents(test_client: TestClient, auth_headers: dict):
    """Test listing documents after upload."""
    file_content = b"Content for list test."
    test_client.post(
        "/api/documents/upload",
        headers=auth_headers,
        files={"file": ("list_test.txt", io.BytesIO(file_content), "text/plain")},
    )
    response = test_client.get("/api/documents", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1


def test_get_document(test_client: TestClient, auth_headers: dict):
    """Test getting a single document."""
    file_content = b"Content for detail test."
    upload_resp = test_client.post(
        "/api/documents/upload",
        headers=auth_headers,
        files={"file": ("detail.txt", io.BytesIO(file_content), "text/plain")},
    )
    doc_id = upload_resp.json()["data"]["id"]

    response = test_client.get(f"/api/documents/{doc_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["id"] == doc_id


def test_get_document_content(test_client: TestClient, auth_headers: dict):
    """Test getting document parsed content."""
    file_content = b"Hello world from test document."
    upload_resp = test_client.post(
        "/api/documents/upload",
        headers=auth_headers,
        files={"file": ("content.txt", io.BytesIO(file_content), "text/plain")},
    )
    doc_id = upload_resp.json()["data"]["id"]

    response = test_client.get(f"/api/documents/{doc_id}/content", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "Hello world" in data["data"]["content"]


def test_delete_document(test_client: TestClient, auth_headers: dict):
    """Test soft deleting a document."""
    file_content = b"Content to delete."
    upload_resp = test_client.post(
        "/api/documents/upload",
        headers=auth_headers,
        files={"file": ("delete.txt", io.BytesIO(file_content), "text/plain")},
    )
    doc_id = upload_resp.json()["data"]["id"]

    response = test_client.delete(f"/api/documents/{doc_id}", headers=auth_headers)
    assert response.status_code == 200

    # Should not be found after deletion
    get_resp = test_client.get(f"/api/documents/{doc_id}", headers=auth_headers)
    assert get_resp.json()["code"] == 404


def test_document_ownership_isolation(test_client: TestClient, db_session, auth_headers):
    """Test that users cannot access each other's documents."""
    from app.utils.jwt import create_access_token
    from app.models.user import User
    from app.utils.password import hash_password

    # Create another user
    other_user = User(username="other", email="other@example.com", password_hash=hash_password("pass123"))
    db_session.add(other_user)
    db_session.commit()
    other_token = create_access_token(data={"sub": other_user.id})
    other_headers = {"Authorization": f"Bearer {other_token}"}

    # Upload document as test user
    file_content = b"My private document."
    upload_resp = test_client.post(
        "/api/documents/upload",
        headers=auth_headers,
        files={"file": ("private.txt", io.BytesIO(file_content), "text/plain")},
    )
    doc_id = upload_resp.json()["data"]["id"]

    # Other user should not see it
    response = test_client.get(f"/api/documents/{doc_id}", headers=other_headers)
    assert response.json()["code"] == 404

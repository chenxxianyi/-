"""Tests for note endpoints."""

from __future__ import annotations

import io

from fastapi.testclient import TestClient


def test_create_note(test_client: TestClient, auth_headers: dict):
    """Test creating a note."""
    payload = {
        "title": "Test Note",
        "content": "<p>This is a test note.</p>",
        "contentType": "richtext",
        "tags": ["test"],
    }
    response = test_client.post("/api/notes", headers=auth_headers, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["data"]["title"] == "Test Note"


def test_list_notes(test_client: TestClient, auth_headers: dict):
    """Test listing notes."""
    # Create two notes
    for i in range(2):
        test_client.post(
            "/api/notes",
            headers=auth_headers,
            json={"title": f"Note {i}", "content": f"<p>Content {i}</p>"},
        )

    response = test_client.get("/api/notes", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 2


def test_update_note(test_client: TestClient, auth_headers: dict):
    """Test updating a note."""
    create_resp = test_client.post(
        "/api/notes",
        headers=auth_headers,
        json={"title": "Original Title", "content": "<p>Original content</p>"},
    )
    note_id = create_resp.json()["data"]["id"]

    update_resp = test_client.put(
        f"/api/notes/{note_id}",
        headers=auth_headers,
        json={"title": "Updated Title"},
    )
    assert update_resp.json()["code"] == 0
    assert update_resp.json()["data"]["title"] == "Updated Title"


def test_delete_note(test_client: TestClient, auth_headers: dict):
    """Test deleting a note."""
    create_resp = test_client.post(
        "/api/notes",
        headers=auth_headers,
        json={"title": "To Delete", "content": "<p>Bye</p>"},
    )
    note_id = create_resp.json()["data"]["id"]

    delete_resp = test_client.delete(f"/api/notes/{note_id}", headers=auth_headers)
    assert delete_resp.json()["code"] == 0

    # Should be gone
    get_resp = test_client.get(f"/api/notes/{note_id}", headers=auth_headers)
    assert get_resp.json()["code"] == 404


def test_create_note_from_annotation(test_client: TestClient, auth_headers: dict):
    """Test creating a note from an annotation."""
    # Upload document
    file_content = b"Selected text for annotation note."
    upload_resp = test_client.post(
        "/api/documents/upload",
        headers=auth_headers,
        files={"file": ("source.txt", io.BytesIO(file_content), "text/plain")},
    )
    doc_id = upload_resp.json()["data"]["id"]

    # Create annotation
    ann_resp = test_client.post(
        f"/api/documents/{doc_id}/annotations",
        headers=auth_headers,
        json={"documentId": doc_id, "selectedText": "Selected text"},
    )
    ann_id = ann_resp.json()["data"]["id"]

    # Create note from annotation
    response = test_client.post(
        "/api/notes/from-annotation",
        headers=auth_headers,
        json={"documentId": doc_id, "sourceAnnotationId": ann_id},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["data"]["sourceAnnotationId"] == ann_id
    assert "Selected text" in data["data"]["excerpt"]


def test_note_ownership_isolation(test_client: TestClient, db_session, auth_headers):
    """Test that users cannot access each other's notes."""
    from app.utils.jwt import create_access_token
    from app.models.user import User
    from app.utils.password import hash_password

    other_user = User(username="other2", email="other2@example.com", password_hash=hash_password("pass123"))
    db_session.add(other_user)
    db_session.commit()
    other_token = create_access_token(data={"sub": other_user.id})
    other_headers = {"Authorization": f"Bearer {other_token}"}

    # Create note as test user
    create_resp = test_client.post(
        "/api/notes",
        headers=auth_headers,
        json={"title": "Private Note", "content": "<p>Secret</p>"},
    )
    note_id = create_resp.json()["data"]["id"]

    # Other user should not see it
    response = test_client.get(f"/api/notes/{note_id}", headers=other_headers)
    assert response.json()["code"] == 404

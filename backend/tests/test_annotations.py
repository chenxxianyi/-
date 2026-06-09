"""Tests for annotation endpoints."""

from __future__ import annotations

import io

from fastapi.testclient import TestClient


def test_create_annotation(test_client: TestClient, auth_headers: dict):
    """Test creating an annotation."""
    # First upload a doc
    file_content = b"Test document for annotations."
    upload_resp = test_client.post(
        "/api/documents/upload",
        headers=auth_headers,
        files={"file": ("ann_test.txt", io.BytesIO(file_content), "text/plain")},
    )
    doc_id = upload_resp.json()["data"]["id"]

    # Create annotation
    payload = {
        "documentId": doc_id,
        "annotationType": "highlight",
        "color": "yellow",
        "selectedText": "test document",
        "note": "A test note",
    }
    response = test_client.post(
        f"/api/documents/{doc_id}/annotations",
        headers=auth_headers,
        json=payload,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["data"]["selectedText"] == "test document"


def test_list_annotations(test_client: TestClient, auth_headers: dict):
    """Test listing annotations for a document."""
    file_content = b"List annotations test."
    upload_resp = test_client.post(
        "/api/documents/upload",
        headers=auth_headers,
        files={"file": ("list_ann.txt", io.BytesIO(file_content), "text/plain")},
    )
    doc_id = upload_resp.json()["data"]["id"]

    # Create two annotations
    for text in ["first annotation", "second annotation"]:
        test_client.post(
            f"/api/documents/{doc_id}/annotations",
            headers=auth_headers,
            json={"documentId": doc_id, "selectedText": text, "color": "blue"},
        )

    response = test_client.get(f"/api/documents/{doc_id}/annotations", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 2


def test_update_annotation(test_client: TestClient, auth_headers: dict):
    """Test updating an annotation."""
    file_content = b"Update annotation test."
    upload_resp = test_client.post(
        "/api/documents/upload",
        headers=auth_headers,
        files={"file": ("update_ann.txt", io.BytesIO(file_content), "text/plain")},
    )
    doc_id = upload_resp.json()["data"]["id"]

    create_resp = test_client.post(
        f"/api/documents/{doc_id}/annotations",
        headers=auth_headers,
        json={"documentId": doc_id, "selectedText": "original", "color": "yellow"},
    )
    ann_id = create_resp.json()["data"]["id"]

    update_resp = test_client.put(
        f"/api/documents/{doc_id}/annotations/{ann_id}",
        headers=auth_headers,
        json={"color": "red", "note": "updated note"},
    )
    assert update_resp.json()["code"] == 0
    assert update_resp.json()["data"]["color"] == "red"


def test_delete_annotation(test_client: TestClient, auth_headers: dict):
    """Test deleting an annotation."""
    file_content = b"Delete annotation test."
    upload_resp = test_client.post(
        "/api/documents/upload",
        headers=auth_headers,
        files={"file": ("del_ann.txt", io.BytesIO(file_content), "text/plain")},
    )
    doc_id = upload_resp.json()["data"]["id"]

    create_resp = test_client.post(
        f"/api/documents/{doc_id}/annotations",
        headers=auth_headers,
        json={"documentId": doc_id, "selectedText": "to delete", "color": "green"},
    )
    ann_id = create_resp.json()["data"]["id"]

    delete_resp = test_client.delete(
        f"/api/documents/{doc_id}/annotations/{ann_id}",
        headers=auth_headers,
    )
    assert delete_resp.json()["code"] == 0

    # Should be gone
    list_resp = test_client.get(f"/api/documents/{doc_id}/annotations", headers=auth_headers)
    assert len(list_resp.json()["data"]) == 0

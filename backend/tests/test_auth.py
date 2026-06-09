"""Tests for auth endpoints."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_health(test_client: TestClient):
    """Test health check endpoint."""
    response = test_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["data"]["status"] == "ok"


def test_register(test_client: TestClient):
    """Test user registration."""
    payload = {
        "username": "newuser",
        "email": "new@example.com",
        "password": "password123",
    }
    response = test_client.post("/api/auth/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert "accessToken" in data["data"]


def test_register_duplicate_email(test_client: TestClient):
    """Test registration with duplicate email."""
    payload = {
        "username": "user1",
        "email": "dup@example.com",
        "password": "password123",
    }
    test_client.post("/api/auth/register", json=payload)
    response = test_client.post("/api/auth/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 409


def test_login(test_client: TestClient):
    """Test login."""
    # First register
    test_client.post("/api/auth/register", json={
        "username": "loginuser",
        "email": "login@example.com",
        "password": "password123",
    })
    # Then login
    response = test_client.post("/api/auth/login", json={
        "email": "login@example.com",
        "password": "password123",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert "accessToken" in data["data"]


def test_login_invalid_credentials(test_client: TestClient):
    """Test login with wrong password."""
    response = test_client.post("/api/auth/login", json={
        "email": "nonexist@example.com",
        "password": "wrongpass",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 401


def test_get_me(test_client: TestClient, auth_headers: dict):
    """Test get current user."""
    response = test_client.get("/api/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["data"]["email"] == "test@example.com"


def test_get_me_unauthorized(test_client: TestClient):
    """Test get current user without token."""
    response = test_client.get("/api/auth/me")
    assert response.status_code == 401

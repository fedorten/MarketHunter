import pytest
from fastapi.testclient import TestClient


class TestGetCurrentUser:
    def test_get_me(self, client, auth_headers, test_user):
        response = client.get("/api/v1/users/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == test_user.username
        assert data["phone"] == test_user.phone
        assert data["email"] == test_user.email

    def test_get_me_unauthorized(self, client):
        response = client.get("/api/v1/users/me")
        assert response.status_code == 401


class TestPatchUser:
    def test_patch_username(self, client, auth_headers):
        response = client.patch(
            "/api/v1/users/me",
            headers=auth_headers,
            json={"username": "NewName"}
        )
        assert response.status_code == 200
        assert response.json()["username"] == "NewName"

    def test_patch_email(self, client, auth_headers):
        response = client.patch(
            "/api/v1/users/me",
            headers=auth_headers,
            json={"email": "newemail@example.com"}
        )
        assert response.status_code == 200
        assert response.json()["email"] == "newemail@example.com"

    def test_patch_unauthorized(self, client):
        response = client.patch(
            "/api/v1/users/me",
            json={"username": "NewName"}
        )
        assert response.status_code == 401

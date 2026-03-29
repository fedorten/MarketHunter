import pytest
from fastapi.testclient import TestClient


class TestRegistration:
    def test_register_new_user(self, client):
        response = client.post(
            "/registration",
            json={
                "username": "NewUser",
                "phone": "+79009999999",
                "password": "password123",
                "email": "newuser@example.com",
            },
        )
        assert response.status_code == 200
        assert response.json() == {"msg": "User created"}

    def test_register_duplicate_phone(self, client, test_user):
        response = client.post(
            "/registration",
            json={
                "username": "AnotherUser",
                "phone": test_user.phone,
                "password": "password123",
            },
        )
        assert response.status_code == 400
        assert "phone" in response.json()["detail"].lower()

    def test_register_duplicate_email(self, client, test_user):
        response = client.post(
            "/registration",
            json={
                "username": "AnotherUser",
                "phone": "+79009999999",
                "password": "password123",
                "email": test_user.email,
            },
        )
        assert response.status_code == 400
        assert "email" in response.json()["detail"].lower()


class TestLogin:
    def test_login_success(self, client, test_user):
        response = client.post(
            "/login", data={"username": test_user.phone, "password": "testpass123"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client, test_user):
        response = client.post(
            "/login", data={"username": test_user.phone, "password": "wrongpassword"}
        )
        assert response.status_code == 401

    def test_login_wrong_phone(self, client):
        response = client.post(
            "/login", data={"username": "+79000000000", "password": "password123"}
        )
        assert response.status_code == 401

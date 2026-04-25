from src.tables import User
from src.routers.secure import get_password_hash


class TestCreateChat:
    def test_create_chat(self, client, db_session, test_user, test_advert):
        user2 = User(
            username="Buyer",
            phone="+79009999999",
            password=get_password_hash("password123")
        )
        db_session.add(user2)
        db_session.commit()
        db_session.refresh(user2)

        login_response = client.post(
            "/login",
            data={"username": user2.phone, "password": "password123"}
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.post(
            f"/api/v1/chats/{test_advert.id}",
            headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "chat_id" in data
        assert data["is_new"] is True

    def test_create_chat_with_own_advert(self, client, auth_headers, test_advert):
        response = client.post(
            f"/api/v1/chats/{test_advert.id}",
            headers=auth_headers
        )
        assert response.status_code == 404

    def test_create_chat_nonexistent_advert(self, client, auth_headers):
        response = client.post(
            "/api/v1/chats/99999",
            headers=auth_headers
        )
        assert response.status_code == 404

def login(client, phone: str, password: str):
    response = client.post("/login", data={"username": phone, "password": password})
    assert response.status_code == 200
    return response.json()["access_token"]


class TestChatMessages:
    def test_create_chat_returns_existing_chat(self, client, db_session, test_advert):
        buyer = User(
            username="Buyer",
            phone="+79009999998",
            password=get_password_hash("password123"),
        )
        db_session.add(buyer)
        db_session.commit()
        db_session.refresh(buyer)
        token = login(client, buyer.phone, "password123")
        headers = {"Authorization": f"Bearer {token}"}

        first = client.post(f"/api/v1/chats/{test_advert.id}", headers=headers)
        second = client.post(f"/api/v1/chats/{test_advert.id}", headers=headers)

        assert first.status_code == 200
        assert second.status_code == 200
        assert second.json()["is_new"] is False
        assert second.json()["chat_id"] == first.json()["chat_id"]

    def test_http_send_message_persists_message(self, client, db_session, test_advert):
        buyer = User(
            username="Buyer",
            phone="+79009999997",
            password=get_password_hash("password123"),
        )
        db_session.add(buyer)
        db_session.commit()
        db_session.refresh(buyer)
        token = login(client, buyer.phone, "password123")
        headers = {"Authorization": f"Bearer {token}"}

        chat_response = client.post(f"/api/v1/chats/{test_advert.id}", headers=headers)
        chat_id = chat_response.json()["chat_id"]

        response = client.post(
            f"/api/v1/chats/{chat_id}/messages",
            headers=headers,
            json={"content": "Здравствуйте"},
        )
        payload = response.json()

        assert response.status_code == 200
        assert payload["chat_id"] == chat_id
        assert payload["sender_id"] == buyer.id
        assert payload["content"] == "Здравствуйте"

        messages = client.get(
            f"/api/v1/chats/{chat_id}/messages", headers=headers
        ).json()
        assert [message["content"] for message in messages] == ["Здравствуйте"]

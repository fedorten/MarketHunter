class TestCreateAdvert:
    def test_create_advert(self, client, auth_headers, test_user):
        response = client.post(
            "/api/v1/adverts/",
            headers=auth_headers,
            json={
                "title": "New Advert",
                "price": 5000,
                "description": "Test description",
                "owner_id": test_user.id
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Advert"
        assert data["price"] == 5000

    def test_create_advert_unauthorized(self, client, test_user):
        response = client.post(
            "/api/v1/adverts/",
            json={
                "title": "New Advert",
                "price": 5000,
                "owner_id": test_user.id
            }
        )
        assert response.status_code == 401


class TestGetAdverts:
    def test_get_all_adverts(self, client, test_advert):
        response = client.get("/api/v1/adverts/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["title"] == test_advert.title

    def test_get_advert_by_id(self, client, test_advert):
        response = client.get(f"/api/v1/adverts/{test_advert.id}")
        assert response.status_code == 200
        assert response.json()["title"] == test_advert.title

    def test_get_nonexistent_advert(self, client):
        response = client.get("/api/v1/adverts/99999")
        assert response.status_code == 404

    def test_get_my_adverts(self, client, auth_headers, test_advert, test_advert2):
        response = client.get("/api/v1/adverts/mine", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert [advert["id"] for advert in data] == [test_advert.id]


class TestPatchAdvert:
    def test_patch_own_advert(self, client, auth_headers, test_advert):
        response = client.patch(
            f"/api/v1/adverts/{test_advert.id}",
            headers=auth_headers,
            json={"price": 7000}
        )
        assert response.status_code == 200
        assert response.json()["price"] == 7000

    def test_patch_other_user_advert(self, client, auth_headers, test_advert2):
        response = client.patch(
            f"/api/v1/adverts/{test_advert2.id}",
            headers=auth_headers,
            json={"price": 7000}
        )
        assert response.status_code == 401


class TestDeleteAdvert:
    def test_delete_own_advert(self, client, auth_headers, test_advert):
        response = client.delete(
            f"/api/v1/adverts/{test_advert.id}",
            headers=auth_headers
        )
        assert response.status_code == 200

    def test_delete_other_user_advert(self, client, auth_headers, test_advert2):
        response = client.delete(
            f"/api/v1/adverts/{test_advert2.id}",
            headers=auth_headers
        )
        assert response.status_code == 401

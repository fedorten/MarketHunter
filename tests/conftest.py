import os
import asyncio

os.environ.setdefault("TESTING", "1")

import pytest
import httpx
from sqlmodel import SQLModel, create_engine, Session
from src.main import app
from src.db import get_session
from src.tables import User, Advert
from src.routers.secure import get_password_hash


TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})


async def override_get_session():
    with Session(test_engine) as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


class ASGITestClient:
    def __init__(self, app):
        self.app = app

    def request(self, method: str, url: str, **kwargs):
        async def run_request():
            transport = httpx.ASGITransport(app=self.app)
            async with httpx.AsyncClient(
                transport=transport, base_url="http://testserver"
            ) as client:
                return await client.request(method, url, **kwargs)

        return asyncio.run(run_request())

    def get(self, url: str, **kwargs):
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs):
        return self.request("POST", url, **kwargs)

    def patch(self, url: str, **kwargs):
        return self.request("PATCH", url, **kwargs)

    def delete(self, url: str, **kwargs):
        return self.request("DELETE", url, **kwargs)


@pytest.fixture(scope="function")
def db_session():
    SQLModel.metadata.drop_all(test_engine)
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session
        session.close()


@pytest.fixture(scope="function")
def client(db_session):
    return ASGITestClient(app)


@pytest.fixture
def test_user(db_session):
    user = User(
        username="TestUser",
        phone="+79001234567",
        password=get_password_hash("testpass123"),
        email="test@example.com"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_user2(db_session):
    user = User(
        username="TestUser2",
        phone="+79001234568",
        password=get_password_hash("testpass123"),
        email="test2@example.com"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_token(client, test_user):
    response = client.post(
        "/login",
        data={"username": test_user.phone, "password": "testpass123"}
    )
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def test_advert(db_session, test_user):
    advert = Advert(
        title="Test Advert",
        price=1000,
        description="Test description",
        owner_id=test_user.id
    )
    db_session.add(advert)
    db_session.commit()
    db_session.refresh(advert)
    return advert


@pytest.fixture
def test_advert2(db_session, test_user2):
    advert = Advert(
        title="Test Advert 2",
        price=2000,
        description="Test description 2",
        owner_id=test_user2.id
    )
    db_session.add(advert)
    db_session.commit()
    db_session.refresh(advert)
    return advert

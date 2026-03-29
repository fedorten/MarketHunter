import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from src.main import app
from src.db import get_session
from src.tables import User, Advert, Chat, Message
from src.routers.secure import get_password_hash


TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})


def override_get_session():
    with Session(test_engine) as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(scope="function")
def db_session():
    SQLModel.metadata.drop_all(test_engine)
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session
        session.close()


@pytest.fixture(scope="function")
def client(db_session):
    return TestClient(app)


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

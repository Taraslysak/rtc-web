import pytest
from typing import Generator
from fastapi import status
from fastapi.testclient import TestClient
from pytest_mock_resources import create_postgres_fixture
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.schemas import User, Token
from app.db import Base, get_db

from tests.mock_data import DUMMY_USERS, fill_mock_data


@pytest.fixture
def client() -> Generator:
    with TestClient(app) as c:
        yield c


db_fixture = create_postgres_fixture()


@pytest.fixture
def db(db_fixture):
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=db_fixture
    )

    Base.metadata.drop_all(bind=db_fixture)
    Base.metadata.create_all(bind=db_fixture)
    with TestingSessionLocal() as db:

        def override_get_db() -> Generator:
            yield db

        app.dependency_overrides[get_db] = override_get_db

        yield db


@pytest.fixture
def authorized_client(client: TestClient, db) -> Generator:
    fill_mock_data(db)
    user = User(**DUMMY_USERS[0])
    assert user
    res = client.post(
        "/auth/login", data=dict(email=user.email, password=user.password)
    )
    assert res.status_code == status.HTTP_200_OK
    token = Token.parse_obj(res.json())
    assert token.access_token
    client.headers.update(
        {
            "Authorization": f"Bearer {token.access_token}",
        }
    )
    return client


@pytest.fixture
def authorized_opponent(client: TestClient, db) -> Generator:
    # fill_mock_data(db)
    user = User(**DUMMY_USERS[1])
    assert user
    res = client.post(
        "/auth/login", data=dict(email=user.email, password=user.password)
    )
    assert res.status_code == status.HTTP_200_OK
    token = Token.parse_obj(res.json())
    assert token.access_token
    client.headers.update(
        {
            "Authorization": f"Bearer {token.access_token}",
        }
    )
    return client

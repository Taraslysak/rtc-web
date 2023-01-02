import pytest
from typing import Generator
from fastapi import status
from fastapi.testclient import TestClient
from pytest_mock_resources import create_redis_fixture
from redis import Redis

from app.main import app
from app.schemas import User, Token
from app.store import get_store

from tests.mock_data import DUMMY_USERS, fill_mock_data


@pytest.fixture
def client() -> Generator:
    with TestClient(app) as c:
        yield c


redis_fixture = create_redis_fixture()


@pytest.fixture
def store(redis_fixture):
    redis = Redis(
        **redis_fixture.pmr_credentials.as_redis_kwargs(), decode_responses=True
    )

    def mock_get_store():
        return redis

    app.dependency_overrides[get_store] = mock_get_store

    yield redis


@pytest.fixture
def authorized_client(client: TestClient, store: Redis) -> Generator:
    fill_mock_data(store)
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

import pytest
from httpx import AsyncClient
from typing import Generator
from fastapi import status
import pytest_asyncio
from fastapi.testclient import TestClient
from pytest_mock_resources import create_redis_fixture
from redis import Redis

from app.app import create_app
from app.schemas import User, Token

from tests.mock_data import DUMMY_USERS, fill_mock_data


redis_fixture = create_redis_fixture()


@pytest_asyncio.fixture
async def client(redis_fixture, monkeypatch: pytest.MonkeyPatch) -> Generator:
    import app.store

    redis = Redis(
        **redis_fixture.pmr_credentials.as_redis_kwargs(), decode_responses=True
    )

    def mock_get_store():
        return redis

    monkeypatch.setattr(app.store, "get_store", mock_get_store)
    app = create_app()
    from app import models

    from redis_om import Migrator

    await Migrator().run()

    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c


@pytest.fixture
def store(client: TestClient, redis_fixture):
    redis = Redis(
        **redis_fixture.pmr_credentials.as_redis_kwargs(), decode_responses=True
    )

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

import pytest
from typing import Generator

from fastapi.testclient import TestClient
from pytest_mock_resources import create_redis_fixture
from redis import Redis

from app.main import app
from app.store import get_store


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

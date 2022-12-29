import pytest
from typing import Generator

from fastapi.testclient import TestClient
from pytest_mock_resources import create_redis_fixture
from redis import Redis

from app.main import app
from app.store import get_store
from tests.mock_data import fill_mock_data


@pytest.fixture
def client() -> Generator:
    with TestClient(app) as c:
        yield c


store = create_redis_fixture()


def mock_store_in_place(app, store):
    def mock_get_store():
        return Redis(**store.pmr_credentials.as_redis_kwargs())

    app.dependency_overrides[get_store] = mock_get_store


# @pytest.fixture
# def store() -> Generator:


#     # generate test data
#     fill_mock_data(store)

#     yield store

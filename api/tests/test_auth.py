from fastapi import status
from fastapi.testclient import TestClient
from redis import Redis

from app.store import get_store
from tests.conftest import mock_store_in_place


def test_register(client: TestClient, store: Redis):
    mock_store_in_place(client.app, store)
    # Test successful registration
    user_data = {
        "username": "foo",
        "email": "foo@bar.com",
        "password": "dummy_password",
    }
    response = client.post("/auth/register", json=user_data)
    assert response
    assert response.status_code == status.HTTP_201_CREATED

    # TODO: Check if user is created id store

    # Test filed registration with same credentials
    fail_response = client.post("/auth/register", json=user_data)
    assert fail_response
    assert fail_response.status_code == status.HTTP_403_FORBIDDEN


def test_login(client: TestClient, store: Redis):
    return


def test_logout(client: TestClient, store: Redis):
    return

from fastapi import status
from fastapi.testclient import TestClient
from redis import Redis
from app.constants import TableNames
from app.schemas.user import User, UserRegister

from app.store import get_store

# from tests.conftest import mock_store_in_place
from tests.mock_data import DUMMY_USERS, fill_mock_data


def test_register(client: TestClient, store: Redis):
    # mock_store_in_place(client.app, store)
    # Test successful registration
    user_data = UserRegister(
        username="foo",
        email="foo@bar.com",
        password="dummy_password",
    )

    response = client.post("/auth/register", json=user_data.dict())
    assert response
    assert response.status_code == status.HTTP_201_CREATED

    # Test filed registration with same credentials
    fail_response = client.post("/auth/register", json=user_data.dict())
    assert fail_response
    assert fail_response.status_code == status.HTTP_403_FORBIDDEN

    user = store.hgetall(f"{TableNames.USERS}:{user_data.email}")
    assert user
    user_model = User(**user)
    assert user_model.username == user_data.username


def test_login(client: TestClient, store: Redis):
    fill_mock_data(store)

    # test login success

    dummy = DUMMY_USERS[0]

    res = client.post(
        "/auth/login",
        data={"username": dummy["username"], "password": dummy["password"]},
    )
    assert res
    assert res.status_code == status.HTTP_200_OK

    data = res.json()
    assert len(data.token) > 0

    user_in_db = store.hgetall(f"{TableNames.USERS}:{dummy['email']}")
    user_model = User(**user_in_db)
    assert user_model.online != 0

    # test wrong username

    res = client.post(
        "/auth/login", data={"username": "BAD_USERNAME", "password": "dummy_password1"}
    )
    assert res
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

    # test wrong password

    res = client.post(
        "/auth/login", data={"username": "user1", "password": "BAD_PASSWORD"}
    )
    assert res
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_logout(client: TestClient, store: Redis):
    return

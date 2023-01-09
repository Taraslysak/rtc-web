from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import models as m
from app.schemas.tokens import Token
from app.schemas.user import User, UserRegister

from tests.mock_data import DUMMY_USERS, fill_mock_data


def test_register(client: TestClient, db: Session):
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

    user = db.query(m.User).filter(m.User.email == user_data.email).first()
    assert user
    user_model = User.from_orm(user)
    assert user_model.username == user_data.username


def test_login(client: TestClient, db: Session):
    fill_mock_data(db)

    # test login success

    dummy = DUMMY_USERS[0]

    res = client.post(
        "/auth/login",
        data={"email": dummy["email"], "password": dummy["password"]},
    )
    assert res
    assert res.status_code == status.HTTP_200_OK

    data = res.json()
    data_schema = Token(**data)
    assert len(data_schema.access_token) > 0

    user_in_db = db.query(m.User).filter(m.User.email == dummy["email"]).first()
    assert user_in_db.logged_in

    # test wrong username

    res = client.post(
        "/auth/login", data={"email": "BAD_USERNAME", "password": "dummy_password1"}
    )
    assert res
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

    # test wrong password

    res = client.post(
        "/auth/login", data={"email": "user1", "password": "BAD_PASSWORD"}
    )
    assert res
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_logout(client: TestClient, db: Session):
    fill_mock_data(db)

    dummy = DUMMY_USERS[0]

    login_res = client.post(
        "/auth/login",
        data={"email": dummy["email"], "password": dummy["password"]},
    )

    data_schema = Token(**login_res.json())

    logout_res = client.post(
        "auth/logout", headers={"Authorization": f"Bearer {data_schema.access_token}"}
    )
    assert logout_res
    assert logout_res.status_code == status.HTTP_200_OK

    user_model = db.query(m.User).filter(m.User.email == dummy["email"]).first()
    assert not user_model.logged_in

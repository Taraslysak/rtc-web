from sqlalchemy.orm import Session

from app import models as m


DUMMY_USERS = [
    {
        "username": "user1",
        "email": "user1@foo.com",
        "password": "dummy_pass1",
        "online": 0,
    },
    {
        "username": "user2",
        "email": "user2@foo.com",
        "password": "dummy_pass2",
        "online": 1,
    },
    {
        "username": "user3",
        "email": "user3@foo.com",
        "password": "dummy_pass3",
        "online": 0,
    },
    {
        "username": "user4",
        "email": "user4@foo.com",
        "password": "dummy_pass4",
        "online": 1,
    },
]


def fill_mock_data(db: Session):
    for user in DUMMY_USERS:
        user_to_add = m.User(**user)
        db.add(user_to_add)
        db.commit()


MOCK_SDP_OFFER = "MOCK_SDP_OFFER"
MOCK_SDP_ANSWER = "MOCK_SDP_ANSWER"

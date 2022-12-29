from redis import Redis
from app.constants import TableNames

from app.schemas.user import User
from app.utils.hash import make_hash

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


def fill_mock_data(store: Redis):
    for user in DUMMY_USERS:
        user_schema = User(**user)
        user_schema.password = make_hash(user_schema.password)
        store.hmset(f"{TableNames.USERS}:{user_schema.email}", user_schema.dict())
    return

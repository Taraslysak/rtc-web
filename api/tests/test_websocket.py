from fastapi.testclient import TestClient
from redis import Redis

from app.constants import TableNames
from app.schemas.tokens import WsToken
from app.schemas.user import User
from tests.mock_data import DUMMY_USERS


def test_websocket_connect(authorized_client: TestClient, store: Redis):
    token_res = authorized_client.get("/ws/token")
    assert token_res
    data = WsToken.parse_obj(token_res.json())
    assert len(data.ws_token) > 0

    with authorized_client.websocket_connect(
        f"/ws/webrtc?token={data.ws_token}",
    ) as websocket:
        data = websocket.receive_json()
        assert data == {
            "users_online": [
                DUMMY_USERS[0]["email"],
                DUMMY_USERS[1]["email"],
                DUMMY_USERS[4]["email"],
            ]
        }
        user = User(store.hgetall(f"{TableNames.USERS}:{DUMMY_USERS[0]['email']}"))
        assert user
        assert user.online

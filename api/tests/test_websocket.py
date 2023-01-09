import json
from fastapi.testclient import TestClient
from redis import Redis
from starlette.testclient import WebSocketTestSession

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
        websocket: WebSocketTestSession = websocket
        data = websocket.receive_json()
        assert data["message_type"] == "users_online"
        online_users = data["payload"]
        online_users.sort()
        assert online_users == [
            DUMMY_USERS[0]["email"],
            DUMMY_USERS[1]["email"],
            DUMMY_USERS[3]["email"],
        ]

        user = User.parse_obj(
            store.hgetall(f"{TableNames.USERS}:{DUMMY_USERS[0]['email']}")
        )
        assert user
        assert user.online
        websocket.send_json(json.dumps({"message_type": "ping"}))
        pong_json = websocket.receive_json()
        pong_data = json.loads(pong_json)
        assert pong_data["message_type"] == "pong"
        # websocket.close()


def test_web_rtc_exchange(authorized_client: TestClient):
    pass

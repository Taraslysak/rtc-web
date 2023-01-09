import json
from fastapi.testclient import TestClient
from starlette.testclient import WebSocketTestSession
from sqlalchemy.orm import Session

from app import models as m
from app.schemas.tokens import WsToken
from tests.mock_data import DUMMY_USERS


def test_websocket_connect(authorized_client: TestClient, db: Session):
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
        assert online_users == [1, 2, 4]

        user = db.query(m.User).filter(m.User.email == DUMMY_USERS[0]["email"]).first()
        assert user
        assert user.online
        websocket.send_json(json.dumps({"message_type": "ping"}))
        pong_json = websocket.receive_json()
        pong_data = json.loads(pong_json)
        assert pong_data["message_type"] == "pong"

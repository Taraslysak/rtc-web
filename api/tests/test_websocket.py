import pytest

from mock import patch
from fastapi.testclient import TestClient
from starlette.testclient import WebSocketTestSession
from sqlalchemy.orm import Session

from app import models as m
from app import schemas as s
from app.routes.ws import connection_service

from tests.mock_data import DUMMY_USERS, MOCK_SDP_OFFER


def test_websocket_connect(authorized_client: TestClient, db: Session):
    token_res = authorized_client.get("/ws/token")
    assert token_res
    data = s.WsToken.parse_obj(token_res.json())
    assert len(data.ws_token) > 0

    with authorized_client.websocket_connect(
        f"/ws/webrtc?token={data.ws_token}",
    ) as websocket:
        websocket: WebSocketTestSession = websocket
        data = s.WsMessage.parse_raw(websocket.receive_json())
        assert data.message_type == s.MessageType.USERS_ONLINE
        online_users = data.payload
        online_users.sort()
        assert online_users == [1, 2, 4]

        user = db.query(m.User).filter(m.User.email == DUMMY_USERS[0]["email"]).first()
        assert user
        assert user.online
        websocket.send_json(s.WsMessage(message_type=s.MessageType.PING).json())
        pong_json = websocket.receive_json()
        pong_data = s.WsMessage.parse_raw(pong_json)
        assert pong_data.message_type == s.MessageType.PONG


@pytest.mark.asyncio
async def test_webrtc_exchange(authorized_client: TestClient, db: Session):
    sender_token_res = authorized_client.get("/ws/token")
    sender_data = s.WsToken.parse_obj(sender_token_res.json())

    wrapped_send_personal = patch.object(
        connection_service,
        "send_personal_message",
        wraps=connection_service.send_personal_message,
    )
    with authorized_client.websocket_connect(
        f"/ws/webrtc?token={sender_data.ws_token}",
    ) as websocket:
        websocket: WebSocketTestSession = websocket
        data = s.WsMessage.parse_raw(websocket.receive_json())
        assert data.message_type == s.MessageType.USERS_ONLINE
        offer_message = s.WsMessage(
            message_type=s.MessageType.PERSONAL,
            payload=s.WebRtcPayload(
                receiver_id=2,
                content=s.OfferContent(
                    sdp=MOCK_SDP_OFFER, type=s.WebRTCContentType.OFFER
                ),
            ),
        )
        websocket.send_json(offer_message.json())
        # TODO: Find a way to check if websocket messages are sent to other user

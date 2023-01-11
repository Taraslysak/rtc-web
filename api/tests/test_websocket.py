import json
from fastapi.testclient import TestClient
from starlette.testclient import WebSocketTestSession
from sqlalchemy.orm import Session

from app import models as m
from app import schemas as s

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


def test_webrtc_exchange(
    authorized_client: TestClient, authorized_opponent: TestClient, db: Session
):
    sender = db.query(m.User).filter(m.User.email == DUMMY_USERS[0]["email"]).first()
    receiver = db.query(m.User).filter(m.User.email == DUMMY_USERS[1]["email"]).first()
    sender_token_res = authorized_client.get("/ws/token")
    data = s.WsToken.parse_obj(sender_token_res.json())

    with authorized_client.websocket_connect(
        f"/ws/webrtc?token={data.ws_token}",
    ) as sender_websocket:
        sender_websocket: WebSocketTestSession = sender_websocket
        receiver_token_res = authorized_opponent.get("/ws/token")
        data = s.WsToken.parse_obj(receiver_token_res.json())

        with authorized_opponent.websocket_connect(
            f"/ws/webrtc?token={data.ws_token}",
        ) as receiver_websocket:
            receiver_websocket: WebSocketTestSession = receiver_websocket

            offer_content = s.OfferContent(
                sdp=MOCK_SDP_OFFER, type=s.WebRTCContentType.OFFER
            )

            offerMessage = s.WsMessage(
                message_type=s.MessageType.PERSONAL,
                payload=s.WebRtcPayload(
                    receiver_id=receiver.id,
                    content=offer_content,
                ),
            )
            sender_websocket.send_json(offerMessage.json())
            receiver_offer_message = receiver_websocket.receive_json()
            assert offerMessage.json() == receiver_offer_message

import json
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app import models as m
from app import schemas as s
from app.db import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.websocket import get_current_ws_user

from app.services.auth import create_access_token
from app.services.web_socket_connection import connection_service
from app.services.web_socket_messageing import MESSAGE_HANDLER
from app.utils.uuid import gen_uid
from app.config import settings


ws_router = APIRouter(prefix="/ws", tags=["ws"])


@ws_router.get("/token")
async def get_ws_token(
    user: m.User = Depends(get_current_user), db: Session = Depends(get_db)
) -> s.WsToken:
    user.connection_id = gen_uid()

    db.commit()
    db.refresh(user)

    ws_token_data = s.WsTokenData(id=user.id, connection_id=user.connection_id)

    ws_token = create_access_token(
        data=ws_token_data.dict(), minutes=settings.WS_TOKEN_EXPIRE_MINUTES
    )

    return s.WsToken(ws_token=ws_token, token_type="Bearer")


@ws_router.websocket("/webrtc")
async def webrtc_websocket(
    websocket: WebSocket,
    current_user: m.User = Depends(get_current_ws_user),
    db: Session = Depends(get_db),
):
    await connection_service.connect(id=current_user.id, websocket=websocket)

    current_user.online = True
    db.commit()
    db.refresh(current_user)

    users_online = db.query(m.User).filter(m.User.online).all()

    broadcast_payload = s.WsMessage(
        message_type=s.MessageType.USERS_ONLINE,
        payload=[user.id for user in users_online],
    )
    await MESSAGE_HANDLER[s.MessageType.USERS_ONLINE](
        broadcast_payload, connection_service, current_user
    )

    try:
        while True:
            ws_json = await websocket.receive_json()
            json_data = s.WsMessage.parse_raw(ws_json)
            await MESSAGE_HANDLER[json_data.message_type](
                json_data, connection_service, current_user
            )

    except WebSocketDisconnect:
        connection_service.disconnect(current_user.connection_id)
        await connection_service.broadcast(
            f"Client #{current_user.email} left the chat"
        )

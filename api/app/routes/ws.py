import json
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, status
from redis import Redis
from app.constants import TableNames
from app.dependencies.auth import get_current_user
from app.dependencies.websocket import get_current_ws_user
from app.schemas.tokens import WsToken, WsTokenData
from app.services.auth import create_access_token
from app.services.web_socket import connection_service
from app.utils.uuid import gen_uid

from app.schemas import User
from app.store import get_store


ws_router = APIRouter(prefix="/ws", tags=["ws"])


@ws_router.get("/token")
async def get_ws_token(
    user: User = Depends(get_current_user), store: Redis = Depends(get_store)
) -> WsToken:
    user.connection_id = gen_uid()

    store.hmset(f"{TableNames.USERS}:{user.email}", user.dict())

    ws_token_data = WsTokenData(email=user.email, connection_id=user.connection_id)

    ws_token = create_access_token(data=ws_token_data.dict(), minutes=1)

    return WsToken(ws_token=ws_token, token_type="Bearer")


@ws_router.websocket("/webrtc")
async def webrtc_websocket(
    websocket: WebSocket,
    current_user: User = Depends(get_current_ws_user),
    store: Redis = Depends(get_store),
):
    await connection_service.connect(email=current_user.email, websocket=websocket)

    current_user.online = 1
    store.hmset(f"{TableNames.USERS}:{current_user.email}", current_user.dict())

    users_keys = store.keys(f"{TableNames.USERS}:*")

    users = [User.parse_obj(store.hgetall(key)) for key in users_keys]

    broadcast_payload = {
        "message_type": "users_online",
        "payload": [user.email for user in users if user.online],
    }

    await connection_service.broadcast(broadcast_payload)
    try:
        while True:
            ws_json = await websocket.receive_json()
            json_data = json.loads(ws_json)
            if json_data["message_type"] == "ping":
                await connection_service.send_personal_message(
                    current_user.email, json.dumps({"message_type": "pong"})
                )
            print(json_data)
    except WebSocketDisconnect:
        connection_service.disconnect(current_user.connection_id)
        await connection_service.broadcast(
            f"Client #{current_user.email} left the chat"
        )

from fastapi import APIRouter, Depends, status
from redis import Redis
from app.constants import TableNames
from app.dependencies.auth import get_current_user
from app.schemas.tokens import WsToken, WsTokenData
from app.services.auth import create_access_token
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
    current_user: User = Depends(get_current_user), store: Redis = Depends(get_store)
):
    # status.WSs
    pass

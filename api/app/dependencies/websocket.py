from fastapi import Depends, Query, WebSocketException, status
from redis import Redis
from app.constants import TableNames
from app.schemas.user import User

from app.services.auth import verify_ws_token
from app.store import get_store

ws_exception = WebSocketException(code=status.WS_1008_POLICY_VIOLATION)


def get_current_ws_user(
    token: str | None = Query(default=None), store: Redis = Depends(get_store)
):
    token_data = verify_ws_token(token, ws_exception)
    user_data = store.hgetall(f"{TableNames.USERS}:{token_data.email}")

    if not user_data:
        raise ws_exception
    user = User.parse_obj(user_data)
    if user.connection_id != token_data.connection_id:
        raise ws_exception

    return user

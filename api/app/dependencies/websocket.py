from fastapi import Depends, Query, WebSocketException, status
from redis import Redis
from app.constants import TableNames
from app.schemas.user import User

from app.services.auth import verify_ws_token
from app.store import get_store

WS_EXCEPTION = WebSocketException(code=status.WS_1008_POLICY_VIOLATION)


def get_current_ws_user(
    token: str | None = Query(default=None), store: Redis = Depends(get_store)
) -> User:
    token_data = verify_ws_token(token, WS_EXCEPTION)
    user_data = store.hgetall(f"{TableNames.USERS}:{token_data.email}")

    if not user_data:
        raise WS_EXCEPTION
    user = User.parse_obj(user_data)
    if user.connection_id != token_data.connection_id:
        raise WS_EXCEPTION

    return user

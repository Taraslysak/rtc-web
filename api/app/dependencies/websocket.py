from fastapi import Depends, Query, WebSocketException, status
from sqlalchemy.orm import Session

from app import models as m

from app.db import get_db
from app.services.auth import verify_ws_token

WS_EXCEPTION = WebSocketException(code=status.WS_1008_POLICY_VIOLATION)


def get_current_ws_user(
    token: str | None = Query(default=None), db: Session = Depends(get_db)
) -> m.User:
    token_data = verify_ws_token(token, WS_EXCEPTION)
    user = db.query(m.User).get(token_data.id)

    if not user or user.connection_id != token_data.connection_id:
        raise WS_EXCEPTION

    return user

from jose import JWTError, jwt
from datetime import datetime, timedelta

from app.schemas import TokenData, WsTokenData
from app.config import settings


SECRET_KEY = settings.JWT_SECRET
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict, minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=minutes)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY)
        id: str = payload.get("id")

        if not id:
            raise credentials_exception

        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def verify_ws_token(token: str, ws_exception) -> WsTokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY)
        id: str = payload.get("id")
        connection_id: str = payload.get("connection_id")

        if not id or not connection_id:
            raise ws_exception

        token_data = WsTokenData(id=id, connection_id=connection_id)
    except JWTError:
        raise ws_exception

    return token_data

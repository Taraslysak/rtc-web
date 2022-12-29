from fastapi import Depends, HTTPException
from redis import Redis
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from app.constants import TableNames

from app.schemas import User, TokenData
from app.store import get_store
from app.config import settings

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=404,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.JWT_SECRET
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY)
        email: str = payload.get("email")

        if not email:
            raise credentials_exception

        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme),
    store: Redis = Depends(get_store),
) -> User:

    token_data: TokenData = verify_access_token(token, CREDENTIALS_EXCEPTION)
    user = store.hgetall(f"{TableNames.USERS}:{token_data.email}")

    if not user:
        raise CREDENTIALS_EXCEPTION

    user_model = User(**user)

    if not user_model.logged_in:
        raise CREDENTIALS_EXCEPTION

    return user_model

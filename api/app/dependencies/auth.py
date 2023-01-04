from fastapi import Depends, HTTPException
from redis import Redis
from fastapi.security import OAuth2PasswordBearer
from app.constants import TableNames
from app.schemas import User, TokenData
from app.services.auth import verify_access_token
from app.store import get_store


CREDENTIALS_EXCEPTION = HTTPException(
    status_code=404,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


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

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.db import SessionLocal, get_db
from app.schemas import TokenData
from app.services.auth import verify_access_token
from app import models as m


CREDENTIALS_EXCEPTION = HTTPException(
    status_code=404,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: SessionLocal = Depends(get_db),
) -> m.User:

    token_data: TokenData = verify_access_token(token, CREDENTIALS_EXCEPTION)
    user = db.query(m.User).get(token_data.id)

    if not user or not user.logged_in:
        raise CREDENTIALS_EXCEPTION

    return user

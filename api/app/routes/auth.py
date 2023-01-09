from fastapi import Depends, status
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db import get_db
from app import models as m
from app.dependencies.auth import get_current_user
from app.forms.register_fom import RegisterRequestForm
from app.logger import log
from app.schemas import UserRegister, TokenData, Token
from app.services.auth import create_access_token
from app.utils.hash import hash_verify

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    try:
        new_user = m.User(**user_data.dict())
        db.add(new_user)
        db.commit()
    except IntegrityError:
        log(log.INFO, "User {} already exists".format(user_data.email))
        db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return


@auth_router.post("/login")
async def login(
    form_data: RegisterRequestForm = Depends(), db: Session = Depends(get_db)
) -> Token:

    user_in_db = db.query(m.User).filter(m.User.email == form_data.email).first()
    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    password_valid = hash_verify(form_data.password, user_in_db.password)
    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    user_in_db.logged_in = True
    db.commit()
    db.refresh(user_in_db)
    return Token(
        access_token=create_access_token(TokenData(id=user_in_db.id).dict()),
        token_type="bearer",
    )


@auth_router.post("/logout")
async def logout(
    user: m.User = Depends(get_current_user), db: Session = Depends(get_db)
):
    user.logged_in = False
    user.online = False
    user.connection_id = ""
    db.commit()
    db.refresh(user)

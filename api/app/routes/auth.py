from redis import Redis, ResponseError
from fastapi import Depends, status
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException

from app.constants import TableNames
from app.dependencies.auth import get_current_user
from app.forms.register_fom import RegisterRequestForm
from app.models.user import MyBoolean
from app.schemas import UserRegister, User, TokenData, Token
from app.services.auth import create_access_token
from app.store import get_store
from app.utils.hash import hash_verify, make_hash
from app import models as m
from app.logger import log

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):

    try:
        user = await m.User.find(m.User.email == user_data.email).first()

        if user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="user already exists"
            )
    except ResponseError as e:
        log(log.INFO, e)
    except Exception as e:
        log(log.INFO, e)
    finally:
        user_data.password = make_hash(user_data.password)
        user_to_save = m.User(
            **user_data.dict(),
            online=MyBoolean.FALSE.value,
            logged_in=MyBoolean.FALSE.value,
        )
        await user_to_save.save()


@auth_router.post("/login")
async def login(
    form_data: RegisterRequestForm = Depends(), store: Redis = Depends(get_store)
) -> Token:

    user_dict = store.hgetall(f"{TableNames.USERS}:{form_data.email}")
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    user_model = User(**user_dict)
    password_valid = hash_verify(form_data.password, user_model.password)
    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    user_model.logged_in = 1
    store.hset(f"{TableNames.USERS}:{form_data.email}", mapping=user_model.dict())
    return Token(
        access_token=create_access_token(TokenData(email=user_model.email).dict()),
        token_type="bearer",
    )


@auth_router.post("/logout")
async def logout(
    user: User = Depends(get_current_user), store: Redis = Depends(get_store)
):
    user.logged_in = 0
    store.hset(f"{TableNames.USERS}:{user.email}", mapping=user.dict())

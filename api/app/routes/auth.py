from redis import Redis
from fastapi import Depends, status
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from app.schemas import UserRegister
from app.schemas.user import UserModel

from app.store import get_store
from app.utils.hash import make_hash

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, store: Redis = Depends(get_store)):

    user = store.exists(f"users:{user_data.email}")

    if user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="user already exists"
        )

    user_data.password = make_hash(user_data.password)
    user_to_save = UserModel(**user_data.dict(), online=0)

    store.hmset(f"users:{user_to_save.email}", user_to_save.dict())

    return

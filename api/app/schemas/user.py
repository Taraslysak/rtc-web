from pydantic import BaseModel, EmailStr, Field


class UserIn(BaseModel):
    username: str
    password: str


class UserRegister(UserIn):
    email: EmailStr


class UserModel(UserRegister):
    online: int

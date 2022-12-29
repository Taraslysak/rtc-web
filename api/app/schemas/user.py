from pydantic import BaseModel, EmailStr


class UserIn(BaseModel):
    username: str
    password: str


class UserRegister(UserIn):
    email: EmailStr


class User(UserRegister):
    online: int
    logged_in: int = 0

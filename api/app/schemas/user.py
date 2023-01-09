from pydantic import BaseModel, EmailStr


class UserIn(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class UserRegister(UserIn):
    email: EmailStr


class User(UserRegister):
    online: int
    logged_in: int = 0
    connection_id: str | None = ""

import enum
from typing import Optional
from pydantic import EmailStr, StrictBool
from redis_om import HashModel, Field
from app.store import get_store


class MyBoolean(enum.StrEnum):
    FALSE = "false"
    TRUE = "true"


class User(HashModel):
    email: EmailStr = Field(index=True)
    password: str
    username: str
    online: str
    logged_in: str
    connection_id: str = ""

    class Meta:
        database = get_store()

    # @property
    # def online(self) -> bool:
    #     return self._online != 0

    # @online.setter
    # def online(self, value: bool):
    #     self._online = 1 if value else 0

    # @property
    # def logged_in(self) -> bool:
    #     return self._logged_in != 0

    # @logged_in.setter
    # def logged_in(self, value: bool):
    #     self._logged_in = 1 if value else 0

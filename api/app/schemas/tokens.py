from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class WsToken(BaseModel):
    ws_token: str
    token_type: str


class TokenData(BaseModel):
    id: str | None


class WsTokenData(TokenData):
    connection_id: str | None

from enum import IntEnum, StrEnum
from pydantic import BaseModel


class MessageType(IntEnum):
    PING = 0
    PONG = 1
    USERS_ONLINE = 2
    PERSONAL = 3


class WebRTCContentType(StrEnum):
    OFFER = "offer"


class OfferContent(BaseModel):
    sdp: str
    type: WebRTCContentType = WebRTCContentType.OFFER


class WebRtcPayload(BaseModel):
    receiver_id: int
    content: OfferContent


class WsMessage(BaseModel):
    message_type: MessageType
    payload: WebRtcPayload | list[int] | None

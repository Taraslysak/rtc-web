from app import schemas as s
from app import models as m
from app.services.types import IConnectionService
from app.logger import log


async def handle_ping(
    _: s.WsMessage, connection_service: IConnectionService, current_user: m.User
):
    await connection_service.send_personal_message(
        current_user.id, s.WsMessage(message_type=s.MessageType.PONG).json()
    )


async def handle_pong(
    _message: s.WsMessage,
    _connection_service: IConnectionService,
    _current_user: m.User,
) -> None:
    log(log.DEBUG, "RECEIVED PONG")


async def handle_broadcast(
    message: s.WsMessage, connection_service: IConnectionService, _: m.User
) -> None:
    await connection_service.broadcast(message.json())


async def handle_retranslate(
    message: s.WsMessage, connection_service: IConnectionService, _: m.User
) -> None:
    await connection_service.send_personal_message(
        message.payload.receiver_id, message=message.json()
    )


MESSAGE_HANDLER = {
    s.MessageType.PING: handle_ping,
    s.MessageType.PONG: handle_pong,
    s.MessageType.PERSONAL: handle_retranslate,
    s.MessageType.USERS_ONLINE: handle_broadcast,
}

from abc import ABC
from typing import Any

from fastapi import WebSocket


class IConnectionService(ABC):
    async def connect(self, id: int, websocket: WebSocket):
        ...

    def disconnect(
        self,
        id: int,
    ):
        ...

    async def send_personal_message(self, id: str, message: str):
        ...

    async def broadcast(self, message: Any):
        ...

from typing import Any
from fastapi import WebSocket


class ConnectionService:
    def __init__(self):
        self.active_connections: dict[str:WebSocket] = {}

    async def connect(self, id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[id] = websocket

    def disconnect(
        self,
        id: int,
    ):
        del self.active_connections[id]

    async def send_personal_message(self, id: str, message: str):
        await self.active_connections[id].send_json(message)

    async def broadcast(self, message: Any):
        for connection in self.active_connections.values():
            await connection.send_json(message)


connection_service = ConnectionService()

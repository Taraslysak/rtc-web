from typing import Any
from fastapi import WebSocket


class ConnectionService:
    def __init__(self):
        self.active_connections: dict[str:WebSocket] = {}

    async def connect(self, email: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[email] = websocket

    def disconnect(
        self,
        email: str,
    ):
        del self.active_connections[email]

    async def send_personal_message(self, email: str, message: Any):
        await self.active_connections[email].send_json(message)

    async def broadcast(self, message: Any):
        for connection in self.active_connections.values():
            await connection.send_json(message)


connection_service = ConnectionService()

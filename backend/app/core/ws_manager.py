from typing import Dict, List
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        # Maps profile_id string -> List of active WebSocket connections
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, profile_id: str):
        await websocket.accept()
        if profile_id not in self.active_connections:
            self.active_connections[profile_id] = []
        self.active_connections[profile_id].append(websocket)

    def disconnect(self, websocket: WebSocket, profile_id: str):
        if profile_id in self.active_connections:
            if websocket in self.active_connections[profile_id]:
                self.active_connections[profile_id].remove(websocket)
            if not self.active_connections[profile_id]:
                del self.active_connections[profile_id]

    async def send_personal_message(self, message: dict, profile_id: str):
        if profile_id in self.active_connections:
            for connection in self.active_connections[profile_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    pass

    async def broadcast(self, message: dict, profile_ids: List[str]):
        for pid in profile_ids:
            await self.send_personal_message(message, pid)

manager = ConnectionManager()

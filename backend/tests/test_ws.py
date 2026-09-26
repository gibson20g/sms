import pytest
from app.core.ws_manager import ConnectionManager

@pytest.mark.asyncio
async def test_ws_connection_manager():
    manager = ConnectionManager()
    profile_id = "test-profile-123"

    class DummyWebSocket:
        def __init__(self):
            self.accepted = False
            self.sent_messages = []

        async def accept(self):
            self.accepted = True

        async def send_json(self, data):
            self.sent_messages.append(data)

    ws = DummyWebSocket()
    await manager.connect(ws, profile_id)
    assert ws.accepted is True
    assert profile_id in manager.active_connections

    await manager.send_personal_message({"event": "ping"}, profile_id)
    assert len(ws.sent_messages) == 1
    assert ws.sent_messages[0]["event"] == "ping"

    manager.disconnect(ws, profile_id)
    assert profile_id not in manager.active_connections

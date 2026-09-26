import uuid
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, status
from app.core.ws_manager import manager

router = APIRouter()

@router.websocket("/ws/chat/{profile_id}")
async def websocket_chat_endpoint(websocket: WebSocket, profile_id: str):
    await manager.connect(websocket, profile_id)
    try:
        while True:
            data = await websocket.receive_json()
            event_type = data.get("event")

            if event_type in ("typing_start", "typing_stop"):
                target_profile_ids = data.get("target_profile_ids", [])
                conversation_id = data.get("conversation_id")
                payload = {
                    "event": event_type,
                    "data": {
                        "conversation_id": conversation_id,
                        "sender_profile_id": profile_id
                    }
                }
                for target_id in target_profile_ids:
                    await manager.send_personal_message(payload, str(target_id))

            elif event_type == "read_receipt":
                target_profile_id = data.get("target_profile_id")
                message_id = data.get("message_id")
                conversation_id = data.get("conversation_id")
                payload = {
                    "event": "read_receipt",
                    "data": {
                        "message_id": message_id,
                        "conversation_id": conversation_id,
                        "reader_profile_id": profile_id,
                        "status": "lido"
                    }
                }
                if target_profile_id:
                    await manager.send_personal_message(payload, str(target_profile_id))

    except WebSocketDisconnect:
        manager.disconnect(websocket, profile_id)
    except Exception:
        manager.disconnect(websocket, profile_id)

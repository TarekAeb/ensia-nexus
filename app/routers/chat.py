from typing import Dict, List, Any
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import json

from app.database import get_db
from app.crud import chat as crud_chat
from app.crud import user as crud_user
from app.schemas import chat as schema_chat
from app.core.security import decode_token
from app.core.auth import get_current_user
from app.models.user import User
from app.config import settings

router = APIRouter(prefix="/chat", tags=["chat"])


class ConnectionManager:
    def __init__(self):
        # roomId -> list of WebSocket connections
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, room_id: int, websocket: WebSocket):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    def disconnect(self, room_id: int, websocket: WebSocket):
        for room_id in list(self.active_connections.keys()):
            if websocket in self.active_connections[room_id]:
                self.active_connections[room_id].remove(websocket)
                if not self.active_connections[room_id]:
                    del self.active_connections[room_id]

    async def broadcast(self, room_id: int, message: Dict[str, Any]):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                try:
                    await connection.send_text(json.dumps(message))
                except Exception:
                    # Handle broken connections
                    pass


manager = ConnectionManager()


@router.get("/rooms", response_model=List[schema_chat.ChatRoomRead])
async def get_rooms(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await crud_chat.get_chat_rooms(db)


@router.post("/rooms", response_model=schema_chat.ChatRoomRead)
async def create_room(room: schema_chat.ChatRoomCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await crud_chat.create_chat_room(db, room)


@router.get("/rooms/{room_id}/messages", response_model=List[schema_chat.ChatMessageRead])
async def get_messages(room_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await crud_chat.get_messages_by_room(db, room_id)


@router.websocket("/ws/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: int,
    db: AsyncSession = Depends(get_db)
):
    # Manual token validation for WebSocket using cookies
    token = websocket.cookies.get(settings.ACCESS_TOKEN_COOKIE_NAME)
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    try:
        payload = decode_token(token)
        user_id = int(payload.get("sub"))
        user = await crud_user.get_user(db, user_id)
        if not user:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
    except Exception:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(room_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Create message in DB
            new_msg_schema = schema_chat.ChatMessageCreate(
                room_id=room_id,
                content=message_data["content"]
            )
            db_msg = await crud_chat.create_chat_message(db, new_msg_schema, user.id)
            
            # Broadcast to all in the room
            broadcast_data = {
                "id": db_msg.id,
                "room_id": db_msg.room_id,
                "sender_user_id": db_msg.sender_user_id,
                "content": db_msg.content,
                "created_at": db_msg.created_at.isoformat(),
                "sender_name": user.full_name
            }
            await manager.broadcast(room_id, broadcast_data)
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(room_id, websocket)

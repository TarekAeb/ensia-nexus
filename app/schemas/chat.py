from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class ChatMessageBase(BaseModel):
    content: str


class ChatMessageCreate(ChatMessageBase):
    room_id: int


class ChatMessageRead(ChatMessageBase):
    id: int
    room_id: int
    sender_user_id: int
    sender_name: Optional[str] = None  # Added for frontend convenience
    created_at: datetime

    class Config:
        from_attributes = True


class ChatRoomBase(BaseModel):
    name: str
    type: str  # 'TEAM' or 'PROJECT'
    project_id: Optional[int] = None


class ChatRoomCreate(ChatRoomBase):
    pass


class ChatRoomRead(ChatRoomBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

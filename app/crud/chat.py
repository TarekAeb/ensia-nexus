from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.chat import ChatRoom, ChatMessage
from app.models.user import User
from app.schemas.chat import ChatRoomCreate, ChatMessageCreate


async def create_chat_room(db: AsyncSession, room: ChatRoomCreate) -> ChatRoom:
    db_room = ChatRoom(
        name=room.name,
        type=room.type,
        project_id=room.project_id
    )
    db.add(db_room)
    await db.commit()
    await db.refresh(db_room)
    return db_room


async def get_chat_rooms(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(ChatRoom).offset(skip).limit(limit))
    return result.scalars().all()


async def get_chat_room_by_id(db: AsyncSession, room_id: int):
    result = await db.execute(select(ChatRoom).filter(ChatRoom.id == room_id))
    return result.scalar_one_or_none()


async def get_chat_rooms_by_project(db: AsyncSession, project_id: int):
    result = await db.execute(select(ChatRoom).filter(ChatRoom.project_id == project_id))
    return result.scalars().all()


async def create_chat_message(db: AsyncSession, message: ChatMessageCreate, sender_id: int) -> ChatMessage:
    db_message = ChatMessage(
        room_id=message.room_id,
        sender_user_id=sender_id,
        content=message.content
    )
    db.add(db_message)
    await db.commit()
    await db.refresh(db_message)
    return db_message


async def get_messages_by_room(db: AsyncSession, room_id: int, skip: int = 0, limit: int = 50):
    result = await db.execute(
        select(ChatMessage, User.full_name.label("sender_name"))
        .join(User, ChatMessage.sender_user_id == User.id)
        .filter(ChatMessage.room_id == room_id)
        .order_by(ChatMessage.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    rows = result.all()
    messages = []
    for row in rows:
        msg = row.ChatMessage
        msg.sender_name = row.sender_name
        messages.append(msg)
    
    return messages[::-1]  # Return in chronological order

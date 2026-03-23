from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


async def get_user(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[User]:
    result = await db.execute(select(User).offset(skip).limit(limit))
    return list(result.scalars().all())


async def create_user(db: AsyncSession, schema: UserCreate) -> User:
    obj = User(**schema.model_dump())
    db.add(obj)
    await db.flush()
    await db.refresh(obj)
    return obj


async def update_user(db: AsyncSession, user_id: int, schema: UserUpdate) -> User | None:
    obj = await get_user(db, user_id)
    if obj is None:
        return None
    for field, value in schema.model_dump(exclude_none=True).items():
        setattr(obj, field, value)
    await db.flush()
    await db.refresh(obj)
    return obj


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    obj = await get_user(db, user_id)
    if obj is None:
        return False
    await db.delete(obj)
    await db.flush()
    return True

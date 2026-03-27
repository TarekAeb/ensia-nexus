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


async def create_user(db: AsyncSession, schema: UserCreate, password: str | None = None) -> User:
    obj = User(**schema.model_dump())
    if password:
        obj.password = password
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


async def update_user_password(db: AsyncSession, user: User, password_hash: str) -> User:
    user.password = password_hash
    user.password_version = (user.password_version or 0) + 1
    await db.flush()
    await db.refresh(user)
    return user

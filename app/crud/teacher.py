from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.teacher import Teacher
from app.schemas.teacher import TeacherCreate, TeacherUpdate


async def get_teacher(db: AsyncSession, user_id: int) -> Teacher | None:
    result = await db.execute(select(Teacher).where(Teacher.user_id == user_id))
    return result.scalar_one_or_none()


async def get_teachers(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Teacher]:
    result = await db.execute(select(Teacher).offset(skip).limit(limit))
    return list(result.scalars().all())


async def create_teacher(db: AsyncSession, schema: TeacherCreate) -> Teacher:
    obj = Teacher(**schema.model_dump())
    db.add(obj)
    await db.flush()
    await db.refresh(obj)
    return obj


async def update_teacher(db: AsyncSession, user_id: int, schema: TeacherUpdate) -> Teacher | None:
    obj = await get_teacher(db, user_id)
    if obj is None:
        return None
    for field, value in schema.model_dump(exclude_none=True).items():
        setattr(obj, field, value)
    await db.flush()
    await db.refresh(obj)
    return obj


async def delete_teacher(db: AsyncSession, user_id: int) -> bool:
    obj = await get_teacher(db, user_id)
    if obj is None:
        return False
    await db.delete(obj)
    await db.flush()
    return True

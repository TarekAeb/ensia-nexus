from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate


async def get_student(db: AsyncSession, user_id: int) -> Student | None:
    result = await db.execute(select(Student).where(Student.user_id == user_id))
    return result.scalar_one_or_none()


async def get_students(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Student]:
    result = await db.execute(select(Student).offset(skip).limit(limit))
    return list(result.scalars().all())


async def create_student(db: AsyncSession, schema: StudentCreate) -> Student:
    obj = Student(**schema.model_dump())
    db.add(obj)
    await db.flush()
    await db.refresh(obj)
    return obj


async def update_student(db: AsyncSession, user_id: int, schema: StudentUpdate) -> Student | None:
    obj = await get_student(db, user_id)
    if obj is None:
        return None
    for field, value in schema.model_dump(exclude_none=True).items():
        setattr(obj, field, value)
    await db.flush()
    await db.refresh(obj)
    return obj


async def delete_student(db: AsyncSession, user_id: int) -> bool:
    obj = await get_student(db, user_id)
    if obj is None:
        return False
    await db.delete(obj)
    await db.flush()
    return True

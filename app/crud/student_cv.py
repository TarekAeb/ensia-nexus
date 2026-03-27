from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.student_cv import StudentCV
from app.schemas.student_cv import StudentCVCreate, StudentCVUpdate


async def get_student_cv(db: AsyncSession, cv_id: int) -> StudentCV | None:
    result = await db.execute(select(StudentCV).where(StudentCV.id == cv_id))
    return result.scalar_one_or_none()


async def get_student_cvs(
    db: AsyncSession,
    student_user_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[StudentCV]:
    query = select(StudentCV)
    if student_user_id is not None:
        query = query.where(StudentCV.student_user_id == student_user_id)
    query = query.order_by(StudentCV.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())


async def create_student_cv(db: AsyncSession, schema: StudentCVCreate) -> StudentCV:
    obj = StudentCV(**schema.model_dump())
    db.add(obj)
    await db.flush()
    await db.refresh(obj)
    return obj


async def update_student_cv(db: AsyncSession, cv_id: int, schema: StudentCVUpdate) -> StudentCV | None:
    obj = await get_student_cv(db, cv_id)
    if obj is None:
        return None
    for field, value in schema.model_dump(exclude_none=True).items():
        setattr(obj, field, value)
    await db.flush()
    await db.refresh(obj)
    return obj


async def delete_student_cv(db: AsyncSession, cv_id: int) -> bool:
    obj = await get_student_cv(db, cv_id)
    if obj is None:
        return False
    await db.delete(obj)
    await db.flush()
    return True

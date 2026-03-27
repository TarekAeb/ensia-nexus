from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.student_previous_project import StudentPreviousProject
from app.schemas.student_previous_project import (
    StudentPreviousProjectCreate,
    StudentPreviousProjectUpdate,
)


async def get_student_previous_project(
    db: AsyncSession, project_id: int
) -> StudentPreviousProject | None:
    result = await db.execute(
        select(StudentPreviousProject).where(StudentPreviousProject.id == project_id)
    )
    return result.scalar_one_or_none()


async def get_student_previous_projects(
    db: AsyncSession,
    student_user_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[StudentPreviousProject]:
    query = select(StudentPreviousProject)
    if student_user_id is not None:
        query = query.where(StudentPreviousProject.student_user_id == student_user_id)
    query = query.order_by(StudentPreviousProject.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())


async def create_student_previous_project(
    db: AsyncSession, schema: StudentPreviousProjectCreate
) -> StudentPreviousProject:
    obj = StudentPreviousProject(**schema.model_dump())
    db.add(obj)
    await db.flush()
    await db.refresh(obj)
    return obj


async def update_student_previous_project(
    db: AsyncSession,
    project_id: int,
    schema: StudentPreviousProjectUpdate,
) -> StudentPreviousProject | None:
    obj = await get_student_previous_project(db, project_id)
    if obj is None:
        return None
    for field, value in schema.model_dump(exclude_none=True).items():
        setattr(obj, field, value)
    await db.flush()
    await db.refresh(obj)
    return obj


async def delete_student_previous_project(db: AsyncSession, project_id: int) -> bool:
    obj = await get_student_previous_project(db, project_id)
    if obj is None:
        return False
    await db.delete(obj)
    await db.flush()
    return True

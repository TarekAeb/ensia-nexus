from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project_application import ProjectApplication
from app.schemas.project_application import ProjectApplicationCreate, ProjectApplicationUpdate


from sqlalchemy.orm import selectinload
from app.models.project import Project


async def get_project_application(db: AsyncSession, app_id: int) -> ProjectApplication | None:
    result = await db.execute(select(ProjectApplication).where(ProjectApplication.id == app_id))
    return result.scalar_one_or_none()


async def get_project_application_for_review(db: AsyncSession, app_id: int) -> ProjectApplication | None:
    result = await db.execute(
        select(ProjectApplication)
        .where(ProjectApplication.id == app_id)
        .options(selectinload(ProjectApplication.project).selectinload(Project.group))
    )
    return result.scalar_one_or_none()


async def get_project_applications(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> list[ProjectApplication]:
    result = await db.execute(select(ProjectApplication).offset(skip).limit(limit))
    return list(result.scalars().all())


async def create_project_application(
    db: AsyncSession, schema: ProjectApplicationCreate
) -> ProjectApplication:
    obj = ProjectApplication(**schema.model_dump())
    db.add(obj)
    await db.flush()
    await db.refresh(obj)
    return obj


async def update_project_application(
    db: AsyncSession, app_id: int, schema: ProjectApplicationUpdate
) -> ProjectApplication | None:
    obj = await get_project_application(db, app_id)
    if obj is None:
        return None
    for field, value in schema.model_dump(exclude_none=True).items():
        setattr(obj, field, value)
    await db.flush()
    await db.refresh(obj)
    return obj


async def delete_project_application(db: AsyncSession, app_id: int) -> bool:
    obj = await get_project_application(db, app_id)
    if obj is None:
        return False
    await db.delete(obj)
    await db.flush()
    return True

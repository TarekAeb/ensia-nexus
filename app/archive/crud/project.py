from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


async def get_project(db: AsyncSession, project_id: int) -> Project | None:
    result = await db.execute(select(Project).where(Project.id == project_id))
    return result.scalar_one_or_none()


async def get_projects(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Project]:
    result = await db.execute(select(Project).offset(skip).limit(limit))
    return list(result.scalars().all())


async def create_project(db: AsyncSession, schema: ProjectCreate) -> Project:
    obj = Project(**schema.model_dump())
    db.add(obj)
    await db.flush()
    await db.refresh(obj)
    return obj


async def update_project(db: AsyncSession, project_id: int, schema: ProjectUpdate) -> Project | None:
    obj = await get_project(db, project_id)
    if obj is None:
        return None
    for field, value in schema.model_dump(exclude_none=True).items():
        setattr(obj, field, value)
    await db.flush()
    await db.refresh(obj)
    return obj


async def delete_project(db: AsyncSession, project_id: int) -> bool:
    obj = await get_project(db, project_id)
    if obj is None:
        return False
    await db.delete(obj)
    await db.flush()
    return True

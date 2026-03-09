from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project_resource import ProjectResource
from app.schemas.project_resource import ProjectResourceCreate, ProjectResourceUpdate


async def get_project_resource(db: AsyncSession, resource_id: int) -> ProjectResource | None:
    result = await db.execute(select(ProjectResource).where(ProjectResource.id == resource_id))
    return result.scalar_one_or_none()


async def get_project_resources(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> list[ProjectResource]:
    result = await db.execute(select(ProjectResource).offset(skip).limit(limit))
    return list(result.scalars().all())


async def create_project_resource(
    db: AsyncSession, schema: ProjectResourceCreate
) -> ProjectResource:
    obj = ProjectResource(**schema.model_dump())
    db.add(obj)
    await db.flush()
    await db.refresh(obj)
    return obj


async def update_project_resource(
    db: AsyncSession, resource_id: int, schema: ProjectResourceUpdate
) -> ProjectResource | None:
    obj = await get_project_resource(db, resource_id)
    if obj is None:
        return None
    for field, value in schema.model_dump(exclude_none=True).items():
        setattr(obj, field, value)
    await db.flush()
    await db.refresh(obj)
    return obj


async def delete_project_resource(db: AsyncSession, resource_id: int) -> bool:
    obj = await get_project_resource(db, resource_id)
    if obj is None:
        return False
    await db.delete(obj)
    await db.flush()
    return True

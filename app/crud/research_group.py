from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.research_group import ResearchGroup
from app.schemas.research_group import ResearchGroupCreate, ResearchGroupUpdate


async def get_research_group(db: AsyncSession, group_id: int) -> ResearchGroup | None:
    result = await db.execute(select(ResearchGroup).where(ResearchGroup.id == group_id))
    return result.scalar_one_or_none()


async def get_research_groups(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[ResearchGroup]:
    result = await db.execute(select(ResearchGroup).offset(skip).limit(limit))
    return list(result.scalars().all())


async def create_research_group(db: AsyncSession, schema: ResearchGroupCreate) -> ResearchGroup:
    obj = ResearchGroup(**schema.model_dump())
    db.add(obj)
    await db.flush()
    await db.refresh(obj)
    return obj


async def update_research_group(db: AsyncSession, group_id: int, schema: ResearchGroupUpdate) -> ResearchGroup | None:
    obj = await get_research_group(db, group_id)
    if obj is None:
        return None
    for field, value in schema.model_dump(exclude_none=True).items():
        setattr(obj, field, value)
    await db.flush()
    await db.refresh(obj)
    return obj


async def delete_research_group(db: AsyncSession, group_id: int) -> bool:
    obj = await get_research_group(db, group_id)
    if obj is None:
        return False
    await db.delete(obj)
    await db.flush()
    return True

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.research_lab import ResearchLab
from app.schemas.research_lab import ResearchLabCreate, ResearchLabUpdate


async def get_research_lab(db: AsyncSession, lab_id: int) -> ResearchLab | None:
    result = await db.execute(select(ResearchLab).where(ResearchLab.id == lab_id))
    return result.scalar_one_or_none()


async def get_research_labs(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[ResearchLab]:
    result = await db.execute(select(ResearchLab).offset(skip).limit(limit))
    return list(result.scalars().all())


async def create_research_lab(db: AsyncSession, schema: ResearchLabCreate) -> ResearchLab:
    obj = ResearchLab(**schema.model_dump())
    db.add(obj)
    await db.flush()
    await db.refresh(obj)
    return obj


async def update_research_lab(db: AsyncSession, lab_id: int, schema: ResearchLabUpdate) -> ResearchLab | None:
    obj = await get_research_lab(db, lab_id)
    if obj is None:
        return None
    for field, value in schema.model_dump(exclude_none=True).items():
        setattr(obj, field, value)
    await db.flush()
    await db.refresh(obj)
    return obj


async def delete_research_lab(db: AsyncSession, lab_id: int) -> bool:
    obj = await get_research_lab(db, lab_id)
    if obj is None:
        return False
    await db.delete(obj)
    await db.flush()
    return True

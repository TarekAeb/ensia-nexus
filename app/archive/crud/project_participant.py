from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project_participant import ProjectParticipant
from app.schemas.project_participant import ProjectParticipantCreate, ProjectParticipantUpdate


async def get_project_participant(
    db: AsyncSession, project_id: int, user_id: int
) -> ProjectParticipant | None:
    result = await db.execute(
        select(ProjectParticipant).where(
            ProjectParticipant.project_id == project_id,
            ProjectParticipant.user_id == user_id,
        )
    )
    return result.scalar_one_or_none()


async def get_project_participants(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> list[ProjectParticipant]:
    result = await db.execute(select(ProjectParticipant).offset(skip).limit(limit))
    return list(result.scalars().all())


async def create_project_participant(
    db: AsyncSession, schema: ProjectParticipantCreate
) -> ProjectParticipant:
    obj = ProjectParticipant(**schema.model_dump())
    db.add(obj)
    await db.flush()
    await db.refresh(obj)
    return obj


async def update_project_participant(
    db: AsyncSession, project_id: int, user_id: int, schema: ProjectParticipantUpdate
) -> ProjectParticipant | None:
    obj = await get_project_participant(db, project_id, user_id)
    if obj is None:
        return None
    for field, value in schema.model_dump(exclude_none=True).items():
        setattr(obj, field, value)
    await db.flush()
    await db.refresh(obj)
    return obj


async def delete_project_participant(
    db: AsyncSession, project_id: int, user_id: int
) -> bool:
    obj = await get_project_participant(db, project_id, user_id)
    if obj is None:
        return False
    await db.delete(obj)
    await db.flush()
    return True

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task_update import TaskUpdate
from app.schemas.task_update import TaskUpdateCreate, TaskUpdateUpdate


async def get_task_update(db: AsyncSession, update_id: int) -> TaskUpdate | None:
    result = await db.execute(select(TaskUpdate).where(TaskUpdate.id == update_id))
    return result.scalar_one_or_none()


async def get_task_updates(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[TaskUpdate]:
    result = await db.execute(select(TaskUpdate).offset(skip).limit(limit))
    return list(result.scalars().all())


async def create_task_update(db: AsyncSession, schema: TaskUpdateCreate) -> TaskUpdate:
    obj = TaskUpdate(**schema.model_dump())
    db.add(obj)
    await db.flush()
    await db.refresh(obj)
    return obj


async def update_task_update(
    db: AsyncSession, update_id: int, schema: TaskUpdateUpdate
) -> TaskUpdate | None:
    obj = await get_task_update(db, update_id)
    if obj is None:
        return None
    for field, value in schema.model_dump(exclude_none=True).items():
        setattr(obj, field, value)
    await db.flush()
    await db.refresh(obj)
    return obj


async def delete_task_update(db: AsyncSession, update_id: int) -> bool:
    obj = await get_task_update(db, update_id)
    if obj is None:
        return False
    await db.delete(obj)
    await db.flush()
    return True

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


async def get_task(db: AsyncSession, task_id: int) -> Task | None:
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.scalar_one_or_none()


async def get_tasks(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Task]:
    result = await db.execute(select(Task).offset(skip).limit(limit))
    return list(result.scalars().all())


async def create_task(db: AsyncSession, schema: TaskCreate) -> Task:
    obj = Task(**schema.model_dump())
    db.add(obj)
    await db.flush()
    await db.refresh(obj)
    return obj


async def update_task(db: AsyncSession, task_id: int, schema: TaskUpdate) -> Task | None:
    obj = await get_task(db, task_id)
    if obj is None:
        return None
    for field, value in schema.model_dump(exclude_none=True).items():
        setattr(obj, field, value)
    await db.flush()
    await db.refresh(obj)
    return obj


async def delete_task(db: AsyncSession, task_id: int) -> bool:
    obj = await get_task(db, task_id)
    if obj is None:
        return False
    await db.delete(obj)
    await db.flush()
    return True

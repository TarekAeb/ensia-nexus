from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import task_update as crud
from app.database import get_db
from app.schemas.task_update import TaskUpdateCreate, TaskUpdateResponse, TaskUpdateUpdate

router = APIRouter(prefix="/task-updates", tags=["task_updates"])


@router.get("/", response_model=list[TaskUpdateResponse])
async def list_task_updates(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_task_updates(db, skip=skip, limit=limit)


@router.get("/{update_id}", response_model=TaskUpdateResponse)
async def get_task_update(update_id: int, db: AsyncSession = Depends(get_db)):
    obj = await crud.get_task_update(db, update_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Task update not found")
    return obj


@router.post("/", response_model=TaskUpdateResponse, status_code=201)
async def create_task_update(schema: TaskUpdateCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_task_update(db, schema)


@router.put("/{update_id}", response_model=TaskUpdateResponse)
async def update_task_update(
    update_id: int, schema: TaskUpdateUpdate, db: AsyncSession = Depends(get_db)
):
    obj = await crud.update_task_update(db, update_id, schema)
    if obj is None:
        raise HTTPException(status_code=404, detail="Task update not found")
    return obj


@router.delete("/{update_id}", status_code=204)
async def delete_task_update(update_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_task_update(db, update_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task update not found")

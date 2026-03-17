from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import task as crud
from app.database import get_db
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskResponse])
async def list_tasks(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_tasks(db, skip=skip, limit=limit)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    obj = await crud.get_task(db, task_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return obj


@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(schema: TaskCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_task(db, schema)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, schema: TaskUpdate, db: AsyncSession = Depends(get_db)):
    obj = await crud.update_task(db, task_id, schema)
    if obj is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return obj


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")

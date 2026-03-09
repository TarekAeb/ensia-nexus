from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import teacher as crud
from app.database import get_db
from app.schemas.teacher import TeacherCreate, TeacherResponse, TeacherUpdate

router = APIRouter(prefix="/teachers", tags=["teachers"])


@router.get("/", response_model=list[TeacherResponse])
async def list_teachers(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_teachers(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=TeacherResponse)
async def get_teacher(user_id: int, db: AsyncSession = Depends(get_db)):
    obj = await crud.get_teacher(db, user_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return obj


@router.post("/", response_model=TeacherResponse, status_code=201)
async def create_teacher(schema: TeacherCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_teacher(db, schema)


@router.put("/{user_id}", response_model=TeacherResponse)
async def update_teacher(user_id: int, schema: TeacherUpdate, db: AsyncSession = Depends(get_db)):
    obj = await crud.update_teacher(db, user_id, schema)
    if obj is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return obj


@router.delete("/{user_id}", status_code=204)
async def delete_teacher(user_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_teacher(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Teacher not found")

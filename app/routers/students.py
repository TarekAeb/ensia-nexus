from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import student as crud
from app.database import get_db
from app.schemas.student import StudentCreate, StudentResponse, StudentUpdate

router = APIRouter(prefix="/students", tags=["students"])


@router.get("/", response_model=list[StudentResponse])
async def list_students(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_students(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=StudentResponse)
async def get_student(user_id: int, db: AsyncSession = Depends(get_db)):
    obj = await crud.get_student(db, user_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return obj


@router.post("/", response_model=StudentResponse, status_code=201)
async def create_student(schema: StudentCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_student(db, schema)


@router.put("/{user_id}", response_model=StudentResponse)
async def update_student(user_id: int, schema: StudentUpdate, db: AsyncSession = Depends(get_db)):
    obj = await crud.update_student(db, user_id, schema)
    if obj is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return obj


@router.delete("/{user_id}", status_code=204)
async def delete_student(user_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_student(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")

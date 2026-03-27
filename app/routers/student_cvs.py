from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import student_cv as crud
from app.database import get_db
from app.schemas.student_cv import StudentCVCreate, StudentCVResponse, StudentCVUpdate

router = APIRouter(prefix="/student-cvs", tags=["student_cvs"])


@router.get("/", response_model=list[StudentCVResponse])
async def list_student_cvs(
    student_user_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    return await crud.get_student_cvs(db, student_user_id=student_user_id, skip=skip, limit=limit)


@router.get("/{cv_id}", response_model=StudentCVResponse)
async def get_student_cv(cv_id: int, db: AsyncSession = Depends(get_db)):
    obj = await crud.get_student_cv(db, cv_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Student CV not found")
    return obj


@router.post("/", response_model=StudentCVResponse, status_code=201)
async def create_student_cv(schema: StudentCVCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_student_cv(db, schema)


@router.put("/{cv_id}", response_model=StudentCVResponse)
async def update_student_cv(cv_id: int, schema: StudentCVUpdate, db: AsyncSession = Depends(get_db)):
    obj = await crud.update_student_cv(db, cv_id, schema)
    if obj is None:
        raise HTTPException(status_code=404, detail="Student CV not found")
    return obj


@router.delete("/{cv_id}", status_code=204)
async def delete_student_cv(cv_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_student_cv(db, cv_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student CV not found")

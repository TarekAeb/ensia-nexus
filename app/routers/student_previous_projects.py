from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import student_previous_project as crud
from app.database import get_db
from app.schemas.student_previous_project import (
    StudentPreviousProjectCreate,
    StudentPreviousProjectResponse,
    StudentPreviousProjectUpdate,
)

router = APIRouter(prefix="/student-previous-projects", tags=["student_previous_projects"])


@router.get("/", response_model=list[StudentPreviousProjectResponse])
async def list_student_previous_projects(
    student_user_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    return await crud.get_student_previous_projects(
        db, student_user_id=student_user_id, skip=skip, limit=limit
    )


@router.get("/{project_id}", response_model=StudentPreviousProjectResponse)
async def get_student_previous_project(
    project_id: int, db: AsyncSession = Depends(get_db)
):
    obj = await crud.get_student_previous_project(db, project_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Student previous project not found")
    return obj


@router.post("/", response_model=StudentPreviousProjectResponse, status_code=201)
async def create_student_previous_project(
    schema: StudentPreviousProjectCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.create_student_previous_project(db, schema)


@router.put("/{project_id}", response_model=StudentPreviousProjectResponse)
async def update_student_previous_project(
    project_id: int,
    schema: StudentPreviousProjectUpdate,
    db: AsyncSession = Depends(get_db),
):
    obj = await crud.update_student_previous_project(db, project_id, schema)
    if obj is None:
        raise HTTPException(status_code=404, detail="Student previous project not found")
    return obj


@router.delete("/{project_id}", status_code=204)
async def delete_student_previous_project(
    project_id: int, db: AsyncSession = Depends(get_db)
):
    deleted = await crud.delete_student_previous_project(db, project_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student previous project not found")

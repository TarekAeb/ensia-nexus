from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import project as crud
from app.database import get_db
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["projects"])


from app.core.auth import get_current_user


@router.get("/", response_model=list[ProjectResponse])
async def list_projects(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await crud.get_projects(db, user=current_user, skip=skip, limit=limit)


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, db: AsyncSession = Depends(get_db)):
    obj = await crud.get_project(db, project_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return obj


@router.post("/", response_model=ProjectResponse, status_code=201)
async def create_project(schema: ProjectCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_project(db, schema)


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: int, schema: ProjectUpdate, db: AsyncSession = Depends(get_db)):
    obj = await crud.update_project(db, project_id, schema)
    if obj is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return obj


@router.delete("/{project_id}", status_code=204)
async def delete_project(project_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_project(db, project_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")

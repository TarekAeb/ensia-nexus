from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import project_resource as crud
from app.database import get_db
from app.schemas.project_resource import (
    ProjectResourceCreate,
    ProjectResourceResponse,
    ProjectResourceUpdate,
)

router = APIRouter(prefix="/project-resources", tags=["project_resources"])


@router.get("/", response_model=list[ProjectResourceResponse])
async def list_resources(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_project_resources(db, skip=skip, limit=limit)


@router.get("/{resource_id}", response_model=ProjectResourceResponse)
async def get_resource(resource_id: int, db: AsyncSession = Depends(get_db)):
    obj = await crud.get_project_resource(db, resource_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Project resource not found")
    return obj


@router.post("/", response_model=ProjectResourceResponse, status_code=201)
async def create_resource(schema: ProjectResourceCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_project_resource(db, schema)


@router.put("/{resource_id}", response_model=ProjectResourceResponse)
async def update_resource(
    resource_id: int, schema: ProjectResourceUpdate, db: AsyncSession = Depends(get_db)
):
    obj = await crud.update_project_resource(db, resource_id, schema)
    if obj is None:
        raise HTTPException(status_code=404, detail="Project resource not found")
    return obj


@router.delete("/{resource_id}", status_code=204)
async def delete_resource(resource_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_project_resource(db, resource_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project resource not found")

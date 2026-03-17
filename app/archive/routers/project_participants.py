from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import project_participant as crud
from app.database import get_db
from app.schemas.project_participant import (
    ProjectParticipantCreate,
    ProjectParticipantResponse,
    ProjectParticipantUpdate,
)

router = APIRouter(prefix="/project-participants", tags=["project_participants"])


@router.get("/", response_model=list[ProjectParticipantResponse])
async def list_participants(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_project_participants(db, skip=skip, limit=limit)


@router.get("/{project_id}/{user_id}", response_model=ProjectParticipantResponse)
async def get_participant(project_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    obj = await crud.get_project_participant(db, project_id, user_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Project participant not found")
    return obj


@router.post("/", response_model=ProjectParticipantResponse, status_code=201)
async def create_participant(schema: ProjectParticipantCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_project_participant(db, schema)


@router.put("/{project_id}/{user_id}", response_model=ProjectParticipantResponse)
async def update_participant(
    project_id: int,
    user_id: int,
    schema: ProjectParticipantUpdate,
    db: AsyncSession = Depends(get_db),
):
    obj = await crud.update_project_participant(db, project_id, user_id, schema)
    if obj is None:
        raise HTTPException(status_code=404, detail="Project participant not found")
    return obj


@router.delete("/{project_id}/{user_id}", status_code=204)
async def delete_participant(project_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_project_participant(db, project_id, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project participant not found")

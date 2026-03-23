from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import project_application as crud
from app.database import get_db
from app.schemas.project_application import (
    ProjectApplicationCreate,
    ProjectApplicationResponse,
    ProjectApplicationUpdate,
)

router = APIRouter(prefix="/project-applications", tags=["project_applications"])


@router.get("/", response_model=list[ProjectApplicationResponse])
async def list_applications(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_project_applications(db, skip=skip, limit=limit)


@router.get("/{app_id}", response_model=ProjectApplicationResponse)
async def get_application(app_id: int, db: AsyncSession = Depends(get_db)):
    obj = await crud.get_project_application(db, app_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Project application not found")
    return obj


@router.post("/", response_model=ProjectApplicationResponse, status_code=201)
async def create_application(schema: ProjectApplicationCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_project_application(db, schema)


from sqlalchemy.orm import selectinload
from app.core.auth import get_current_user
from app.models.project import Project
from app.models.research_group import ResearchGroup


@router.put("/{app_id}", response_model=ProjectApplicationResponse)
async def update_application(
    app_id: int, 
    schema: ProjectApplicationUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Fetch application with project and group info
    application = await crud.get_project_application_for_review(db, app_id)
    
    if application is None:
        raise HTTPException(status_code=404, detail="Project application not found")
        
    # Authorization check: only project leader, group leader, or creator
    project = application.project
    group_leader_id = project.group.leader_user_id
    project_creator_id = project.created_by
    
    is_authorized = current_user.id in [group_leader_id, project_creator_id] or current_user.role == "ADMIN"
    
    if not is_authorized:
        raise HTTPException(
            status_code=403, 
            detail="Only project leader or group record leader can review applications"
        )

    obj = await crud.update_project_application(db, app_id, schema)
    return obj


@router.delete("/{app_id}", status_code=204)
async def delete_application(app_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_project_application(db, app_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project application not found")

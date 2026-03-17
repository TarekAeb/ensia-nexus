from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.domains.projects.schemas import ProjectCreate, ProjectUpdate, ProjectResponse, ParticipantCreate, \
    ParticipantResponse
from app.domains.projects import controller as project_controller

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.get("/", response_model=List[ProjectResponse])
def list_projects():
    return project_controller.list_projects()


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int):
    return project_controller.get_project(project_id)


# Spec: POST /groups/{group_id}/projects -> create project in group
@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(project_data: ProjectCreate):
    # Need group_id, presumably in body or query if we don't route via /groups/{id}/projects
    return project_controller.create_project(project_data)


@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project_data: ProjectUpdate):
    return project_controller.update_project(project_id, project_data)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int):
    return project_controller.delete_project(project_id)


@router.get("/{project_id}/participants", response_model=List[ParticipantResponse])
def list_participants(project_id: int):
    return project_controller.list_participants(project_id)


@router.post("/{project_id}/participants", response_model=ParticipantResponse)
def add_participant(project_id: int, participant_data: ParticipantCreate):
    return project_controller.add_participant(project_id, participant_data)


@router.delete("/{project_id}/participants/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_participant(project_id: int, user_id: int):
    return project_controller.remove_participant(project_id, user_id)

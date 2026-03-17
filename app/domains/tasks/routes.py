from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.domains.tasks.schemas import TaskCreate, TaskUpdate, TaskResponse, TaskUpdateCreate, TaskUpdateResponse
from app.domains.tasks import controller as task_controller

router = APIRouter(
    prefix="/projects/{project_id}/tasks",
    tags=["Tasks"]
)


# Spec: GET /projects/{project_id}/tasks
@router.get("/", response_model=List[TaskResponse])
def list_tasks(project_id: int):
    return task_controller.list_tasks(project_id)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    return task_controller.get_task(task_id)


# Spec: POST /projects/{project_id}/tasks
@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate):
    # project_id needed
    return task_controller.create_task(task_data)


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskUpdate):
    return task_controller.update_task(task_id, task_data)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    return task_controller.delete_task(task_id)


@router.post("/{task_id}/updates", response_model=TaskUpdateResponse)
def add_task_update(task_id: int, update_data: TaskUpdateCreate):
    return task_controller.add_task_update(task_id, update_data)


@router.get("/{task_id}/updates", response_model=List[TaskUpdateResponse])
def list_task_updates(task_id: int):
    return task_controller.list_task_updates(task_id)

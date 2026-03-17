from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.domains.resources.schemas import ResourceCreate, ResourceResponse
from app.domains.resources import controller as resource_controller

router = APIRouter(
    prefix="/resources",
    tags=["Resources"]
)


# Spec: GET /projects/{project_id}/resources
@router.get("/", response_model=List[ResourceResponse])
def list_resources(project_id: int):
    return resource_controller.list_resources(project_id)


# Spec: POST /projects/{project_id}/resources
@router.post("/", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
def add_resource(resource_data: ResourceCreate):
    # project_id needed
    return resource_controller.add_resource(resource_data)


@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(resource_id: int):
    return resource_controller.delete_resource(resource_id)

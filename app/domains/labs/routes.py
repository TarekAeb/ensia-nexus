from fastapi import APIRouter, status
from typing import List
from app.domains.labs.schemas import LabCreate, LabUpdate, LabResponse
from app.domains.labs import controller as lab_controller

router = APIRouter(
    prefix="/labs",
    tags=["Labs"]
)


# GET    /labs                                list all research labs
@router.get("/", response_model=List[LabResponse])
def list_labs():
    return lab_controller.list_labs()


# GET    /labs/{lab_id}                       get lab details
@router.get("/{lab_id}", response_model=LabResponse)
def get_lab(lab_id: int):
    return lab_controller.get_lab(lab_id)


# POST   /labs                                create new research lab
@router.post("/", response_model=LabResponse, status_code=status.HTTP_201_CREATED)
def create_lab(lab_data: LabCreate):
    return lab_controller.create_lab(lab_data)


# PATCH  /labs/{lab_id}                       update lab information
@router.patch("/{lab_id}", response_model=LabResponse)
def update_lab(lab_id: int, lab_data: LabUpdate):
    return lab_controller.update_lab(lab_id, lab_data)


# DELETE /labs/{lab_id}                       delete lab
@router.delete("/{lab_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lab(lab_id: int):
    return lab_controller.delete_lab(lab_id)

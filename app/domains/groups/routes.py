from fastapi import APIRouter, status
from typing import List
from app.domains.groups.schemas import GroupCreate, GroupUpdate, GroupResponse
from app.domains.users.schemas import UserResponse  # Assuming member list returns UserResponse
from app.domains.groups import controller as group_controller

# Base router for groups
router = APIRouter(
    prefix="/groups",
    tags=["Groups"]
)


@router.get("/", response_model=List[GroupResponse])
def list_groups():
    return group_controller.list_groups()


@router.get("/{group_id}", response_model=GroupResponse)
def get_group(group_id: int):
    return group_controller.get_group(group_id)


@router.post("/", response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
def create_group(group_data: GroupCreate):
    return group_controller.create_group(group_data)


@router.patch("/{group_id}", response_model=GroupResponse)
def update_group(group_id: int, group_data: GroupUpdate):
    return group_controller.update_group(group_id, group_data)


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(group_id: int):
    pass


@router.post("/{group_id}/members", response_model=GroupResponse)  # Or maybe MemberResponse
def add_member(group_id: int, user_id: int):
    pass


@router.delete("/{group_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_member(group_id: int, user_id: int):
    pass


@router.get("/{group_id}/members", response_model=List[UserResponse])
def list_members(group_id: int):
    pass


@router.patch("/{group_id}/validate", response_model=GroupResponse)
def validate_group(group_id: int):
    pass

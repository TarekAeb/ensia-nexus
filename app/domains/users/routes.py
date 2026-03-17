from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.domains.users.schemas import UserResponse, UserUpdate
from app.domains.users import controller as user_controller

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me", response_model=UserResponse)
def get_my_profile():
    return user_controller.get_my_profile()


@router.patch("/me", response_model=UserResponse)
def update_my_profile(profile_data: UserUpdate):
    return user_controller.update_my_profile(profile_data)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    return user_controller.get_user(user_id)


@router.get("/", response_model=List[UserResponse])
def list_users():
    return user_controller.list_users()


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    return user_controller.delete_user(user_id)

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.core.auth import get_current_user
from app.domains.users.schemas import UserResponse, UserUpdate
from app.domains.users import controller as user_controller

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user=Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "role": current_user.role,
        "institution": current_user.institution,
        "department": current_user.department,
        "contact_email": current_user.contact_email,
        "phone_number": current_user.phone_number,
        "address": current_user.address,
        "website": current_user.website,
        "email_verified": current_user.email_verified,
        "created_at": current_user.created_at
    }

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

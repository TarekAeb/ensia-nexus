from fastapi import APIRouter, Depends, HTTPException, status, Response

from app.core.auth import get_current_user
from app.domains.auth.schemas import UserSignup, UserLogin, Token, UserResponse, UserPasswordChange
from app.domains.auth.controller import sign_up, log_in, change_password as change_password_controller

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/signup",
             response_model=UserResponse,
             status_code=status.HTTP_201_CREATED)
def signup(user_data: UserSignup, response: Response):
    return sign_up(user_data, response)


@router.post("/login", response_model=UserResponse)
def login(credentials: UserLogin, response: Response):
    return log_in(credentials, response)


@router.delete("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout():
    return


@router.post("/refresh", response_model=UserResponse)
def refresh_token():
    return


@router.patch("/password", response_model=UserResponse)
def change_password(
        data: UserPasswordChange,
        current_user=Depends(get_current_user)
):
    return change_password_controller(data, current_user)

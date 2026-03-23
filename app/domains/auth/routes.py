from fastapi import APIRouter, Depends, HTTPException, status

from app.core.auth import get_current_user
from app.domains.auth.schemas import UserSignup, UserLogin, Token, UserResponse
from app.domains.auth.controller import sign_up, log_in

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/signup",
             response_model=UserResponse,
             status_code=status.HTTP_201_CREATED)
def signup(user_data: UserSignup):
    return sign_up(user_data)


@router.post("/login", response_model=Token)
def login(credentials: UserLogin):
    return log_in(credentials)


@router.delete("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout():
    return


@router.post("/refresh", response_model=Token)
def refresh_token():
    return


@router.patch("/password", response_model=UserResponse)
def change_password(
        data: UserLogin,
        current_user=Depends(get_current_user)
):
    return change_password(data, current_user)

from fastapi import APIRouter, Depends, HTTPException, status
from app.domains.auth.schemas import UserSignup, UserLogin, Token, UserResponse
from app.domains.auth.controller import sign_up, log_in, get_current_user_info

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/signup", response_model=UserResponse)
def signup(user_data: UserSignup):
    return sign_up()


@router.post("/login", response_model=Token)
def login(credentials: UserLogin):
    return log_in()


@router.get("/me", response_model=UserResponse)
def get_current_user():
    return get_current_user_info()

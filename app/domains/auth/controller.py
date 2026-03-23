from fastapi import HTTPException
from app.domains.auth.service import AuthService
from app.domains.auth.schemas import UserSignup as SignSch, UserLogin as LoginSch


def sign_up():
    return AuthService.signup()


def log_in(data: LoginSch):
    try:
        return AuthService.login(data)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


def get_current_user_info():
    return AuthService.get_current_user()

from fastapi import HTTPException
from app.domains.auth.service import AuthService


def sign_up():
    return AuthService.signup()


def log_in():
    return AuthService.login()


def get_current_user_info():
    return AuthService.get_current_user()

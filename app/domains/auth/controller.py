from fastapi import HTTPException
from fastapi import Response

from app.archive.config import settings
from app.domains.auth.service import AuthService
from app.domains.auth.schemas import (UserSignup as SignSch,
                                      UserLogin as LoginSch,
                                      UserPasswordChange as PassChangeSch)

COOKIE_CONFIG = {
    "httponly": True,
    "secure": settings.env == "production",
    "samesite": "Strict"
}


def build_auth_response(response: Response, user, access_token: str, refresh_token: str):
    """
    Sets auth cookies and returns user response.
    """

    # Access token cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=60 * 15,  # 15 minutes
        **COOKIE_CONFIG
    )

    # Refresh token cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=60 * 60 * 24 * 7,  # 7 days
        **COOKIE_CONFIG
    )

    # Response body (no tokens)
    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name
        }
    }


def sign_up(data: SignSch, response: Response):
    try:

        # 1. Create user
        user = AuthService.signup(data)

        # 2. Generate tokens
        tokens = AuthService.generate_token(user.id)

        # 3. Build response with cookies
        return build_auth_response(response, user, tokens[0], tokens[1])

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


def log_in(data: LoginSch, response: Response):
    try:

        user = AuthService.login(data)

        # 2. Generate tokens
        tokens = AuthService.generate_token(user.id)

        # 3. Build response with cookies
        return build_auth_response(response, user, tokens[0], tokens[1])

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


def get_current_user_info():
    return AuthService.get_current_user()


def change_password(data: PassChangeSch, current_user):
    try:

        # 1. Change password
        AuthService.change_password(data, current_user)

        # 2. opionally disconnect all sessions (not implemented yet)

        # 3. generate new token
        token = AuthService.generate_token(current_user.id)

        # 4. send email notification (not implemented yet)

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": current_user.id,
                "email": current_user.email,
                "full_name": current_user.full_name
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

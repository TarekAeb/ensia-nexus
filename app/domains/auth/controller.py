from fastapi import HTTPException
from app.domains.auth.service import AuthService
from app.domains.auth.schemas import (UserSignup as SignSch,
                                      UserLogin as LoginSch,
                                      UserPasswordChange as PassChangeSch)


def sign_up(data: SignSch):
    try:

        # 1. Create user
        user = AuthService.signup(data)

        # 2. Generate token
        token = AuthService.generate_token(user.id)

        # 3. Return response 201
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name
            }
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


def log_in(data: LoginSch):
    try:

        user = AuthService.login(data)

        token = AuthService.generate_token(user.id)

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name
            }
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


def get_current_user_info():
    return AuthService.get_current_user()


def change_password(data: PassChangeSch, current_user):
    try:

        # 1. Change password
        AuthService.change_password(current_user, data)

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

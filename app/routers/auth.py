from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.core.auth import get_current_user, get_refresh_token, login_with_google
from app.core.security import (
    verify_password,
    generate_tokens,
    hash_password,
    generate_reset_token,
    decode_token,
)
from app.core.email import send_password_reset_email
from app.crud import user as crud
from app.schemas.auth import (
    UserSignup,
    UserLogin,
    UserResponse,
    UserPasswordChange,
    GoogleLoginRequest,
    ForgotPasswordRequest,
    ResetPasswordConfirmRequest,
)
from app.schemas.user import UserCreate

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)



@router.get("/me", response_model=UserResponse)
async def get_me(current_user=Depends(get_current_user)):
    return current_user


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserSignup, response: Response, db: AsyncSession = Depends(get_db)):
    # 1. Check if user already exists
    existing_user = await crud.get_user_by_email(db, email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2. Hash password
    password_hash = hash_password(user_data.password)

    # 3. Create user
    user = await crud.create_user(
        db,
        crud.UserCreate(
            email=user_data.email,
            full_name=user_data.full_name,
            role=user_data.role
        ),
        password=password_hash
    )

    # 4. Generate tokens
    access_token, refresh_token = generate_tokens(user.id)

    # 5. Set cookies
    response.set_cookie(key=settings.ACCESS_TOKEN_COOKIE_NAME, value=access_token, httponly=True)
    response.set_cookie(key=settings.REFRESH_TOKEN_COOKIE_NAME, value=refresh_token, httponly=True)

    return user


@router.post("/login", response_model=UserResponse)
async def login(credentials: UserLogin, response: Response, db: AsyncSession = Depends(get_db)):
    # 1. Get user
    user = await crud.get_user_by_email(db, email=credentials.email)
    if not user or not user.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # 2. Verify password
    if not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # 3. Generate tokens
    access_token, refresh_token = generate_tokens(user.id)

    # 4. Set cookies
    response.set_cookie(key=settings.ACCESS_TOKEN_COOKIE_NAME, value=access_token, httponly=True)
    response.set_cookie(key=settings.REFRESH_TOKEN_COOKIE_NAME, value=refresh_token, httponly=True)

    return user


@router.delete("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response):
    response.status_code = status.HTTP_204_NO_CONTENT
    response.delete_cookie(settings.ACCESS_TOKEN_COOKIE_NAME)
    response.delete_cookie(settings.REFRESH_TOKEN_COOKIE_NAME)
    return response


@router.patch("/password", response_model=UserResponse)
async def change_password(
        data: UserPasswordChange,
        current_user=Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    # 1. Verify old password
    if not verify_password(data.old_password, current_user.password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    # 2. Hash new password
    new_password_hash = hash_password(data.new_password)

    # 3. Update user
    await crud.update_user_password(db, current_user, new_password_hash)

    return current_user


# @router.post("/refresh", response_model=UserResponse) # WHY DID YOU DELETE THIS ???

@router.post("/google", response_model=UserResponse)
async def google_login(data: GoogleLoginRequest, response: Response, db: AsyncSession = Depends(get_db)):
    # 1. Verify Google token and get user info
    user = await login_with_google(db, data.id_token)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid Google token")

    # 2 Generate tokens
    access_token, refresh_token = generate_tokens(user.id)

    # 3. Set cookies
    response.set_cookie(key=settings.ACCESS_TOKEN_COOKIE_NAME, value=access_token, httponly=True)
    response.set_cookie(key=settings.REFRESH_TOKEN_COOKIE_NAME, value=refresh_token, httponly=True)

    return user


@router.post("/forget_password", status_code=status.HTTP_200_OK)
async def forget_password(data: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user_by_email(db, email=str(data.email))

    # Always return success to avoid disclosing whether an email exists.
    if user and user.password:
        reset_token = generate_reset_token(user.id, user.password_version or 0)
        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
        send_password_reset_email(user.email, reset_link)

    return {"message": "If the email exists, a reset link has been sent."}


@router.post("/reset_password_confirm", response_model=UserResponse)
async def reset_password_confirm(
    data: ResetPasswordConfirmRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    payload = decode_token(data.token)

    if payload.get("type") != "reset":
        raise HTTPException(status_code=400, detail="Invalid token type")

    user_id = payload.get("sub")
    token_password_version = payload.get("pv")
    if user_id is None or token_password_version is None:
        raise HTTPException(status_code=400, detail="Invalid token payload")

    user = await crud.get_user(db, int(user_id))
    if not user:
        raise HTTPException(status_code=400, detail="Invalid reset token")

    if (user.password_version or 0) != int(token_password_version):
        raise HTTPException(status_code=400, detail="Reset token is no longer valid")

    if not data.new_password or len(data.new_password) < 8:
        raise HTTPException(
            status_code=400,
            detail="New password must be at least 8 characters long",
        )

    try:
        new_password_hash = hash_password(data.new_password)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid password") from exc
    await crud.update_user_password(db, user, new_password_hash)

    access_token, refresh_token = generate_tokens(user.id)
    response.set_cookie(key=settings.ACCESS_TOKEN_COOKIE_NAME, value=access_token, httponly=True)
    response.set_cookie(key=settings.REFRESH_TOKEN_COOKIE_NAME, value=refresh_token, httponly=True)

    return user

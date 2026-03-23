from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.core.auth import get_current_user, get_refresh_token
from app.core.security import verify_password, generate_tokens, hash_password
from app.crud import user as crud
from app.schemas.auth import UserSignup, UserLogin, UserResponse, UserPasswordChange

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

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
            role="STUDENT" # default role
        )
    )
    user.password = password_hash
    await db.flush()
    await db.refresh(user)

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
    response.delete_cookie(settings.ACCESS_TOKEN_COOKIE_NAME)
    response.delete_cookie(settings.REFRESH_TOKEN_COOKIE_NAME)
    return response

@router.patch("/password", response_model=UserResponse)
async def change_password(
    data: UserPasswordChange,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # 1. Verify old password
    if not verify_password(data.old_password, current_user.password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    # 2. Hash new password
    new_password_hash = hash_password(data.new_password)

    # 3. Update user
    current_user.password = new_password_hash
    await db.flush()
    await db.refresh(current_user)

    return current_user

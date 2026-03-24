from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.core.auth import get_current_user, get_refresh_token
from app.core.security import verify_password, generate_tokens, hash_password
from app.crud import user as crud
from app.schemas.auth import UserSignup, UserLogin, UserResponse, UserPasswordChange, UserGoogleLogin
from app.schemas.user import UserCreate

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/google", response_model=UserResponse)
async def google_auth(
    data: UserGoogleLogin,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    """
    Handle Google OAuth authentication (Mock implementation).
    In a real scenario, this would verify the Google id_token.
    """
    # 1. Try to find user by provided data or use a default mock user
    user = None
    if data.user_id:
        user = await crud.get_user(db, data.user_id)
    elif data.email:
        user = await crud.get_user_by_email(db, data.email)
    
    # 2. If user doesn't exist, create a mock Google user
    if not user:
        email = data.email or "google_test@ensia.edu.dz"
        full_name = data.full_name or "Google Test User"
        
        # Check if email exists again (in case user_id was wrong)
        user = await crud.get_user_by_email(db, email)
        if not user:
            user = await crud.create_user(
                db,
                UserCreate(
                    email=email,
                    full_name=full_name,
                    role="STUDENT"
                )
            )

    # 3. Generate tokens
    access_token, refresh_token = generate_tokens(user.id)
    
    # 4. Set cookies
    response.set_cookie(key=settings.ACCESS_TOKEN_COOKIE_NAME, value=access_token, httponly=True)
    response.set_cookie(key=settings.REFRESH_TOKEN_COOKIE_NAME, value=refresh_token, httponly=True)

    return user

@router.get("/me", response_model=UserResponse)
async def get_me(current_user = Depends(get_current_user)):
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
    await crud.update_user_password(db, current_user, new_password_hash)

    return current_user

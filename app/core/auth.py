from fastapi import Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import decode_token
from app.crud import user as crud
from app.database import get_db
from app.config import settings


async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)):
    # 1. Try cookie first
    token = request.cookies.get(settings.ACCESS_TOKEN_COOKIE_NAME)

    # 2. Fallback to Authorization header
    if not token:
        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

    # 3. No token found
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # 4. Decode token
    try:
        payload = decode_token(token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    # 5. Validate token type
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid token type")

    # 6. Get user
    user_id = int(payload.get("sub"))
    user = await crud.get_user(db, user_id)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def get_refresh_token(request: Request):
    # 1. Try cookie first
    token = request.cookies.get("refresh_token")

    # 2. Fallback to Authorization header
    if not token:
        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

    # 3. No token found
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return token

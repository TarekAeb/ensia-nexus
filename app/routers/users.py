from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import user as crud
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse])
async def list_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    obj = await crud.get_user(db, user_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="User not found")
    return obj


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(schema: UserCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_user(db, schema)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, schema: UserUpdate, db: AsyncSession = Depends(get_db)):
    obj = await crud.update_user(db, user_id, schema)
    if obj is None:
        raise HTTPException(status_code=404, detail="User not found")
    return obj


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")

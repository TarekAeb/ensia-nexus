from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import group_member as crud
from app.database import get_db
from app.schemas.group_member import GroupMemberCreate, GroupMemberResponse, GroupMemberUpdate

router = APIRouter(prefix="/group-members", tags=["group_members"])


@router.get("/", response_model=list[GroupMemberResponse])
async def list_group_members(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_group_members(db, skip=skip, limit=limit)


@router.get("/{group_id}/{user_id}", response_model=GroupMemberResponse)
async def get_group_member(group_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    obj = await crud.get_group_member(db, group_id, user_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Group member not found")
    return obj


@router.post("/", response_model=GroupMemberResponse, status_code=201)
async def create_group_member(schema: GroupMemberCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_group_member(db, schema)


@router.put("/{group_id}/{user_id}", response_model=GroupMemberResponse)
async def update_group_member(
    group_id: int, user_id: int, schema: GroupMemberUpdate, db: AsyncSession = Depends(get_db)
):
    obj = await crud.update_group_member(db, group_id, user_id, schema)
    if obj is None:
        raise HTTPException(status_code=404, detail="Group member not found")
    return obj


@router.delete("/{group_id}/{user_id}", status_code=204)
async def delete_group_member(group_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_group_member(db, group_id, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Group member not found")

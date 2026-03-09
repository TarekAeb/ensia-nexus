from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import research_group as crud
from app.database import get_db
from app.schemas.research_group import ResearchGroupCreate, ResearchGroupResponse, ResearchGroupUpdate

router = APIRouter(prefix="/groups", tags=["research_groups"])


@router.get("/", response_model=list[ResearchGroupResponse])
async def list_groups(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_research_groups(db, skip=skip, limit=limit)


@router.get("/{group_id}", response_model=ResearchGroupResponse)
async def get_group(group_id: int, db: AsyncSession = Depends(get_db)):
    obj = await crud.get_research_group(db, group_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Research group not found")
    return obj


@router.post("/", response_model=ResearchGroupResponse, status_code=201)
async def create_group(schema: ResearchGroupCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_research_group(db, schema)


@router.put("/{group_id}", response_model=ResearchGroupResponse)
async def update_group(group_id: int, schema: ResearchGroupUpdate, db: AsyncSession = Depends(get_db)):
    obj = await crud.update_research_group(db, group_id, schema)
    if obj is None:
        raise HTTPException(status_code=404, detail="Research group not found")
    return obj


@router.delete("/{group_id}", status_code=204)
async def delete_group(group_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_research_group(db, group_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Research group not found")

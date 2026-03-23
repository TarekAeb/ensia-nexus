from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import research_lab as crud
from app.database import get_db
from app.schemas.research_lab import ResearchLabCreate, ResearchLabResponse, ResearchLabUpdate

router = APIRouter(prefix="/labs", tags=["research_labs"])


@router.get("/", response_model=list[ResearchLabResponse])
async def list_labs(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_research_labs(db, skip=skip, limit=limit)


@router.get("/{lab_id}", response_model=ResearchLabResponse)
async def get_lab(lab_id: int, db: AsyncSession = Depends(get_db)):
    obj = await crud.get_research_lab(db, lab_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Research lab not found")
    return obj


@router.post("/", response_model=ResearchLabResponse, status_code=201)
async def create_lab(schema: ResearchLabCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_research_lab(db, schema)


@router.put("/{lab_id}", response_model=ResearchLabResponse)
async def update_lab(lab_id: int, schema: ResearchLabUpdate, db: AsyncSession = Depends(get_db)):
    obj = await crud.update_research_lab(db, lab_id, schema)
    if obj is None:
        raise HTTPException(status_code=404, detail="Research lab not found")
    return obj


@router.delete("/{lab_id}", status_code=204)
async def delete_lab(lab_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_research_lab(db, lab_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Research lab not found")

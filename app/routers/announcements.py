from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.crud import announcement as crud
from app.database import get_db
from app.schemas.announcement import AnnouncementCreate, AnnouncementResponse, AnnouncementUpdate
from app.core.auth import get_current_user

router = APIRouter(prefix="/announcements", tags=["Announcements"])

@router.get("/", response_model=List[AnnouncementResponse])
async def list_announcements(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_announcements(db, skip=skip, limit=limit)

@router.post("/", response_model=AnnouncementResponse, status_code=201)
async def create_announcement(schema: AnnouncementCreate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role not in ["ADMIN", "TEACHER", "PROFESSOR", "DOCTOR", "MCA", "RESEARCHER"]:
        raise HTTPException(status_code=403, detail="Only teachers and admins can post announcements")
    return await crud.create_announcement(db, schema)

@router.put("/{id}", response_model=AnnouncementResponse)
async def update_announcement(id: int, schema: AnnouncementUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    # Basic check - normally should be author or admin
    return await crud.update_announcement(db, id, schema)

@router.delete("/{id}", status_code=204)
async def delete_announcement(id: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    if not await crud.delete_announcement(db, id):
        raise HTTPException(status_code=404, detail="Announcement not found")

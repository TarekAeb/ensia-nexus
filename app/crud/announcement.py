from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from app.models.announcement import Announcement, AnnouncementComment, AnnouncementReaction
from app.schemas.announcement import AnnouncementCreate, AnnouncementUpdate, CommentCreate, ReactionCreate

async def get_announcements(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Announcement]:
    result = await db.execute(select(Announcement).offset(skip).limit(limit).order_by(Announcement.created_at.desc()))
    return result.scalars().all()

async def create_announcement(db: AsyncSession, schema: AnnouncementCreate) -> Announcement:
    obj = Announcement(**schema.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def update_announcement(db: AsyncSession, id: int, schema: AnnouncementUpdate) -> Optional[Announcement]:
    result = await db.execute(select(Announcement).filter(Announcement.id == id))
    obj = result.scalar_one_or_none()
    if not obj:
        return None
    for key, value in schema.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    await db.commit()
    await db.refresh(obj)
    return obj

async def delete_announcement(db: AsyncSession, id: int) -> bool:
    result = await db.execute(select(Announcement).filter(Announcement.id == id))
    obj = result.scalar_one_or_none()
    if not obj:
        return False
    await db.delete(obj)
    await db.commit()
    return True


# --- Comments ---
async def get_comments(db: AsyncSession, announcement_id: int) -> List[AnnouncementComment]:
    result = await db.execute(
        select(AnnouncementComment)
        .filter(AnnouncementComment.announcement_id == announcement_id)
        .order_by(AnnouncementComment.created_at.asc())
    )
    return result.scalars().all()

async def create_comment(db: AsyncSession, schema: CommentCreate) -> AnnouncementComment:
    obj = AnnouncementComment(**schema.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def delete_comment(db: AsyncSession, id: int) -> bool:
    result = await db.execute(select(AnnouncementComment).filter(AnnouncementComment.id == id))
    obj = result.scalar_one_or_none()
    if not obj:
        return False
    await db.delete(obj)
    await db.commit()
    return True

# --- Reactions ---
async def get_reactions(db: AsyncSession, announcement_id: int) -> List[AnnouncementReaction]:
    result = await db.execute(
        select(AnnouncementReaction)
        .filter(AnnouncementReaction.announcement_id == announcement_id)
    )
    return result.scalars().all()

async def toggle_reaction(db: AsyncSession, schema: ReactionCreate) -> Optional[AnnouncementReaction]:
    # Check if exists
    result = await db.execute(
        select(AnnouncementReaction).filter(
            AnnouncementReaction.announcement_id == schema.announcement_id,
            AnnouncementReaction.user_id == schema.user_id
        )
    )
    obj = result.scalar_one_or_none()
    
    if obj:
        if obj.reaction_type == schema.reaction_type:
            # Same reaction - remove it
            await db.delete(obj)
            await db.commit()
            return None
        else:
            # Different reaction - update it
            obj.reaction_type = schema.reaction_type
            await db.commit()
            await db.refresh(obj)
            return obj
    else:
        # Create new
        new_obj = AnnouncementReaction(**schema.model_dump())
        db.add(new_obj)
        await db.commit()
        await db.refresh(new_obj)
        return new_obj

async def get_interaction_summary(db: AsyncSession, announcement_id: int, user_id: Optional[int] = None) -> dict:
    # Comments count
    c_res = await db.execute(select(func.count()).select_from(AnnouncementComment).filter(AnnouncementComment.announcement_id == announcement_id))
    comments_count = c_res.scalar() or 0
    
    # Reactions
    r_res = await db.execute(select(AnnouncementReaction).filter(AnnouncementReaction.announcement_id == announcement_id))
    reactions = r_res.scalars().all()
    
    reactions_count = len(reactions)
    reactions_by_type = {}
    user_reacted = None
    
    for r in reactions:
        reactions_by_type[r.reaction_type] = reactions_by_type.get(r.reaction_type, 0) + 1
        if user_id and r.user_id == user_id:
            user_reacted = r.reaction_type
            
    return {
        "comments_count": comments_count,
        "reactions_count": reactions_count,
        "reactions_by_type": reactions_by_type,
        "user_reacted": user_reacted
    }


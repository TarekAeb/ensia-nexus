from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.group_member import GroupMember
from app.schemas.group_member import GroupMemberCreate, GroupMemberUpdate


async def get_group_member(db: AsyncSession, group_id: int, user_id: int) -> GroupMember | None:
    result = await db.execute(
        select(GroupMember).where(
            GroupMember.group_id == group_id, GroupMember.user_id == user_id
        )
    )
    return result.scalar_one_or_none()


async def get_group_members(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[GroupMember]:
    result = await db.execute(select(GroupMember).offset(skip).limit(limit))
    return list(result.scalars().all())


async def create_group_member(db: AsyncSession, schema: GroupMemberCreate) -> GroupMember:
    obj = GroupMember(**schema.model_dump())
    db.add(obj)
    await db.flush()
    await db.refresh(obj)
    return obj


async def update_group_member(
    db: AsyncSession, group_id: int, user_id: int, schema: GroupMemberUpdate
) -> GroupMember | None:
    obj = await get_group_member(db, group_id, user_id)
    if obj is None:
        return None
    for field, value in schema.model_dump(exclude_none=True).items():
        setattr(obj, field, value)
    await db.flush()
    await db.refresh(obj)
    return obj


async def delete_group_member(db: AsyncSession, group_id: int, user_id: int) -> bool:
    obj = await get_group_member(db, group_id, user_id)
    if obj is None:
        return False
    await db.delete(obj)
    await db.flush()
    return True

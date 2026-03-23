from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


async def get_project(db: AsyncSession, project_id: int) -> Project | None:
    result = await db.execute(select(Project).where(Project.id == project_id))
    return result.scalar_one_or_none()


from app.models.user import User
from app.models.group_member import GroupMember
from sqlalchemy import or_


async def get_projects(db: AsyncSession, user: User, skip: int = 0, limit: int = 100) -> list[Project]:
    # Students can see PUBLIC projects OR PRIVATE projects if they are members of the group
    # Admins/Teachers might have different rules, but for now let's follow the provided rule:
    # "Visibility: Projects can be designated as Public (visible to all students) or Private (restricted to specific group members)."
    
    if user.role == "ADMIN":
        query = select(Project)
    else:
        # Get groups where user is a member
        member_groups_query = select(GroupMember.group_id).where(GroupMember.user_id == user.id, GroupMember.is_active == True)
        member_groups_result = await db.execute(member_groups_query)
        member_group_ids = [r[0] for r in member_groups_result.all()]
        
        query = select(Project).where(
            or_(
                Project.visibility == "PUBLIC",
                Project.group_id.in_(member_group_ids)
            )
        )
    
    result = await db.execute(query.offset(skip).limit(limit))
    return list(result.scalars().all())


async def create_project(db: AsyncSession, schema: ProjectCreate) -> Project:
    obj = Project(**schema.model_dump())
    db.add(obj)
    await db.flush()
    await db.refresh(obj)
    return obj


async def update_project(db: AsyncSession, project_id: int, schema: ProjectUpdate) -> Project | None:
    obj = await get_project(db, project_id)
    if obj is None:
        return None
    for field, value in schema.model_dump(exclude_none=True).items():
        setattr(obj, field, value)
    await db.flush()
    await db.refresh(obj)
    return obj


async def delete_project(db: AsyncSession, project_id: int) -> bool:
    obj = await get_project(db, project_id)
    if obj is None:
        return False
    await db.delete(obj)
    await db.flush()
    return True

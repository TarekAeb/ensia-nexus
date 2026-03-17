from app.core.database import SessionLocal
from app.infrastructure.database.models.group_model import ResearchGroup
from app.infrastructure.database.models.group_member_model import GroupMember
from sqlalchemy import text


class GroupRepository:

    @staticmethod
    def get_group(group_id: int):
        with SessionLocal() as db:
            return db.query(ResearchGroup).filter(ResearchGroup.id == group_id).first()

    @staticmethod
    def list_groups():
        with SessionLocal() as db:
            return db.query(ResearchGroup).all()

    @staticmethod
    def create_group(group_data):
        with SessionLocal() as db:
            group = ResearchGroup(**group_data.dict())
            db.add(group)
            db.commit()
            db.refresh(group)
            return group

    @staticmethod
    def update_group(group_id: int, group_data):
        with SessionLocal() as db:
            group = db.query(ResearchGroup).filter(ResearchGroup.id == group_id).first()
            if group:
                for key, value in group_data.dict(exclude_unset=True).items():
                    setattr(group, key, value)
                db.commit()
                db.refresh(group)
            return group

    @staticmethod
    def add_member(group_id: int, user_id: int):
        with SessionLocal() as db:
            member = GroupMember(group_id=group_id, user_id=user_id)
            db.add(member)
            db.commit()
            return member

    @staticmethod
    def remove_member(group_id: int, user_id: int):
        with SessionLocal() as db:
            member = db.query(GroupMember).filter(
                GroupMember.group_id == group_id,
                GroupMember.user_id == user_id
            ).first()
            if member:
                db.delete(member)
                db.commit()
                return True
            return False

    @staticmethod
    def is_member(group_id: int, user_id: int):
         with SessionLocal() as db:
            member = db.query(GroupMember).filter(
                GroupMember.group_id == group_id,
                GroupMember.user_id == user_id,
                GroupMember.is_active == True
            ).first()
            return member is not None

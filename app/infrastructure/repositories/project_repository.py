from app.core.database import SessionLocal
from app.infrastructure.database.models.project_model import Project
from app.infrastructure.database.models.project_participant_model import ProjectParticipant


class ProjectRepository:

    @staticmethod
    def get_project(project_id: int):
        with SessionLocal() as db:
            return db.query(Project).filter(Project.id == project_id).first()

    @staticmethod
    def list_projects():
        with SessionLocal() as db:
            return db.query(Project).all()

    @staticmethod
    def create_project(project_data):
        with SessionLocal() as db:
            project = Project(**project_data.dict())
            db.add(project)
            db.commit()
            db.refresh(project)
            return project

    @staticmethod
    def update_project(project_id: int, project_data):
        with SessionLocal() as db:
            project = db.query(Project).filter(Project.id == project_id).first()
            if project:
                for key, value in project_data.dict(exclude_unset=True).items():
                    setattr(project, key, value)
                db.commit()
                db.refresh(project)
            return project

    @staticmethod
    def delete_project(project_id: int):
        with SessionLocal() as db:
            project = db.query(Project).filter(Project.id == project_id).first()
            if project:
                db.delete(project)
                db.commit()
                return True
            return False

    @staticmethod
    def add_participant(project_id: int, user_id: int, role: str = 'MEMBER'):
        with SessionLocal() as db:
            participant = ProjectParticipant(project_id=project_id, user_id=user_id, participant_role=role)
            db.add(participant)
            db.commit()
            return participant

    @staticmethod
    def remove_participant(project_id: int, user_id: int):
        with SessionLocal() as db:
            participant = db.query(ProjectParticipant).filter(
                ProjectParticipant.project_id == project_id,
                ProjectParticipant.user_id == user_id
            ).first()
            if participant:
                db.delete(participant)
                db.commit()
                return True
            return False

    @staticmethod
    def is_project_member(project_id: int, user_id: int):
        with SessionLocal() as db:
            return db.query(ProjectParticipant).filter(
                ProjectParticipant.project_id == project_id,
                ProjectParticipant.user_id == user_id
            ).first() is not None

    @staticmethod
    def list_participants(project_id: int):
        with SessionLocal() as db:
            return db.query(ProjectParticipant).filter(ProjectParticipant.project_id == project_id).all()

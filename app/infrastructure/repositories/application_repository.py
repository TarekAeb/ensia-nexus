from app.core.database import SessionLocal
from app.infrastructure.database.models.project_application_model import ProjectApplication


class ApplicationRepository:

    @staticmethod
    def get_application(application_id: int):
        with SessionLocal() as db:
            return db.query(ProjectApplication).filter(ProjectApplication.id == application_id).first()

    @staticmethod
    def get_applications_by_project(project_id: int):
        with SessionLocal() as db:
            return db.query(ProjectApplication).filter(ProjectApplication.project_id == project_id).all()

    @staticmethod
    def get_my_applications(student_user_id: int):
        with SessionLocal() as db:
            return db.query(ProjectApplication).filter(ProjectApplication.student_user_id == student_user_id).all()

    @staticmethod
    def create_application(application_data):
        with SessionLocal() as db:
            application = ProjectApplication(**application_data.dict())
            db.add(application)
            db.commit()
            db.refresh(application)
            return application

    @staticmethod
    def update_application_status(application_id: int, status: str):
        with SessionLocal() as db:
            application = db.query(ProjectApplication).filter(ProjectApplication.id == application_id).first()
            if application:
                application.status = status
                db.commit()
                db.refresh(application)
            return application



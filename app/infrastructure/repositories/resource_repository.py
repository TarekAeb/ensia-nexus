from app.core.database import SessionLocal
from app.infrastructure.database.models.project_resource_model import ProjectResource


class ResourceRepository:

    @staticmethod
    def get_resource(resource_id: int):
        with SessionLocal() as db:
            return db.query(ProjectResource).filter(ProjectResource.id == resource_id).first()

    @staticmethod
    def list_resources(project_id: int):
        with SessionLocal() as db:
            return db.query(ProjectResource).filter(ProjectResource.project_id == project_id).all()

    @staticmethod
    def create_resource(resource_data):
        with SessionLocal() as db:
            resource = ProjectResource(**resource_data.dict())
            db.add(resource)
            db.commit()
            db.refresh(resource)
            return resource

    @staticmethod
    def delete_resource(resource_id: int):
        with SessionLocal() as db:
            resource = db.query(ProjectResource).filter(ProjectResource.id == resource_id).first()
            if resource:
                db.delete(resource)
                db.commit()
                return True
            return False



from app.core.database import SessionLocal
from app.infrastructure.database.models.lab_model import ResearchLab


class LabRepository:

    @staticmethod
    def get_lab(lab_id: int):
        with SessionLocal() as db:
            return db.query(ResearchLab).filter(ResearchLab.id == lab_id).first()

    @staticmethod
    def list_labs():
        with SessionLocal() as db:
            return db.query(ResearchLab).all()

    @staticmethod
    def create_lab(lab_data):
        with SessionLocal() as db:
            lab = ResearchLab(**lab_data.dict())
            db.add(lab)
            db.commit()
            db.refresh(lab)
            return lab

    @staticmethod
    def update_lab(lab_id: int, lab_data):
        with SessionLocal() as db:
            lab = db.query(ResearchLab).filter(ResearchLab.id == lab_id).first()
            if lab:
                for key, value in lab_data.dict(exclude_unset=True).items():
                    setattr(lab, key, value)
                db.commit()
                db.refresh(lab)
            return lab

    @staticmethod
    def delete_lab(lab_id: int):
        with SessionLocal() as db:
            lab = db.query(ResearchLab).filter(ResearchLab.id == lab_id).first()
            if lab:
                db.delete(lab)
                db.commit()
                return True
            return False



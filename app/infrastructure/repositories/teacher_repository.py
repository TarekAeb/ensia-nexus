from app.core.database import SessionLocal
from app.infrastructure.database.models.teacher_model import Teacher


class TeacherRepository:

    @staticmethod
    def get_teacher(user_id: int):
        with SessionLocal() as db:
            return db.query(Teacher).filter(Teacher.user_id == user_id).first()

    @staticmethod
    def create_teacher_profile(teacher_data):
        with SessionLocal() as db:
            teacher = Teacher(**teacher_data.dict())
            db.add(teacher)
            db.commit()
            db.refresh(teacher)
            return teacher

    @staticmethod
    def update_teacher_profile(user_id: int, teacher_data):
        with SessionLocal() as db:
            teacher = db.query(Teacher).filter(Teacher.user_id == user_id).first()
            if teacher:
                for key, value in teacher_data.dict(exclude_unset=True).items():
                    setattr(teacher, key, value)
                db.commit()
                db.refresh(teacher)
            return teacher

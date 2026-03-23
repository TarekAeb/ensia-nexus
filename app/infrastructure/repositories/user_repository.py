from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.infrastructure.database.models.user_model import User
from app.infrastructure.database.models.student_model import Student
from app.infrastructure.database.models.teacher_model import Teacher


class UserRepository:

    @staticmethod
    def get_user_by_id(user_id: int):
        with SessionLocal() as db:
            return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(email: str):
        with SessionLocal() as db:
            return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create_user(user_data):
        with SessionLocal() as db:
            user = User(**user_data)
            db.add(user)
            db.commit()
            db.refresh(user)
            return user

    @staticmethod
    def create_student_profile(student_data):
        with SessionLocal() as db:
            student = Student(**student_data)
            db.add(student)
            db.commit()
            db.refresh(student)
            return student

    @staticmethod
    def create_teacher_profile(teacher_data):
        with SessionLocal() as db:
            teacher = Teacher(**teacher_data)
            db.add(teacher)
            db.commit()
            db.refresh(teacher)
            return teacher

    @staticmethod
    def update_user(user_id: int, data: dict):
        with SessionLocal() as db:
            try:
                user = db.query(User).filter(User.id == user_id).first()

                if not user:
                    return None

                for key, value in data.items():
                    setattr(user, key, value)

                db.commit()
                db.refresh(user)

                return user

            except Exception:
                db.rollback()
                raise

    @staticmethod
    def delete_user(user_id: int):
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                db.delete(user)
                db.commit()
                return True
            return False

    @staticmethod
    def list_users():
        with SessionLocal() as db:
            return db.query(User).order_by(User.created_at.desc()).all()

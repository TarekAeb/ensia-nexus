from app.core.database import SessionLocal
from app.infrastructure.database.models.task_model import Task
from app.infrastructure.database.models.task_update_model import TaskUpdate


class TaskRepository:

    @staticmethod
    def get_task(task_id: int):
        with SessionLocal() as db:
            return db.query(Task).filter(Task.id == task_id).first()

    @staticmethod
    def list_tasks(project_id: int):
        with SessionLocal() as db:
            return db.query(Task).filter(Task.project_id == project_id).all()

    @staticmethod
    def create_task(task_data):
        with SessionLocal() as db:
            task = Task(**task_data.dict())
            db.add(task)
            db.commit()
            db.refresh(task)
            return task

    @staticmethod
    def update_task(task_id: int, task_data):
        with SessionLocal() as db:
            task = db.query(Task).filter(Task.id == task_id).first()
            if task:
                for key, value in task_data.dict(exclude_unset=True).items():
                    setattr(task, key, value)
                db.commit()
                db.refresh(task)
            return task

    @staticmethod
    def delete_task(task_id: int):
         with SessionLocal() as db:
            task = db.query(Task).filter(Task.id == task_id).first()
            if task:
                db.delete(task)
                db.commit()
                return True
            return False

    @staticmethod
    def create_task_update(update_data):
        with SessionLocal() as db:
            update = TaskUpdate(**update_data.dict())
            db.add(update)
            db.commit()
            db.refresh(update)
            return update

    @staticmethod
    def list_task_updates(task_id: int):
        with SessionLocal() as db:
            return db.query(TaskUpdate).filter(TaskUpdate.task_id == task_id).all()



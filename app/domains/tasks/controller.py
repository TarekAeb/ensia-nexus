from app.domains.tasks.service import TaskService
from app.domains.tasks.schemas import TaskCreate, TaskUpdate, TaskUpdateCreate


def list_tasks(project_id: int):
    return TaskService.list_tasks(project_id)


def get_task(task_id: int):
    return TaskService.get_task(task_id)


def create_task(task_data: TaskCreate):
    return TaskService.create_task(task_data)


def update_task(task_id: int, task_data: TaskUpdate):
    return TaskService.update_task(task_id, task_data)


def delete_task(task_id: int):
    return TaskService.delete_task(task_id)


def add_task_update(task_id: int, update_data: TaskUpdateCreate):
    return TaskService.add_task_update(task_id, update_data)


def list_task_updates(task_id: int):
    return TaskService.list_task_updates(task_id)

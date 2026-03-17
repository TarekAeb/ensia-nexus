from datetime import date, datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict


TaskStatus = Literal["TODO", "IN_PROGRESS", "BLOCKED", "DONE", "CANCELLED"]
TaskPriority = Literal["LOW", "MEDIUM", "HIGH", "URGENT"]


class TaskBase(BaseModel):
    project_id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus = "TODO"
    priority: TaskPriority = "MEDIUM"
    created_by: Optional[int] = None
    assignee_user_id: Optional[int] = None
    due_date: Optional[date] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee_user_id: Optional[int] = None
    due_date: Optional[date] = None


class TaskResponse(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

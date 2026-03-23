from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TaskUpdateBase(BaseModel):
    task_id: int
    author_user_id: Optional[int] = None
    note: Optional[str] = None
    hours_added: float = 0
    new_status: Optional[str] = None
    new_progress: Optional[int] = None


class TaskUpdateCreate(TaskUpdateBase):
    pass


class TaskUpdateUpdate(BaseModel):
    note: Optional[str] = None
    hours_added: Optional[float] = None
    new_status: Optional[str] = None
    new_progress: Optional[int] = None


class TaskUpdateResponse(TaskUpdateBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: Optional[datetime] = None

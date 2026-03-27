from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class StudentPreviousProjectBase(BaseModel):
    title: str
    project_link: Optional[str] = None
    description: Optional[str] = None


class StudentPreviousProjectCreate(StudentPreviousProjectBase):
    student_user_id: int


class StudentPreviousProjectUpdate(BaseModel):
    title: Optional[str] = None
    project_link: Optional[str] = None
    description: Optional[str] = None


class StudentPreviousProjectResponse(StudentPreviousProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_user_id: int
    created_at: Optional[datetime] = None

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict


ApplicationStatus = Literal["PENDING", "ACCEPTED", "REJECTED"]


class ProjectApplicationBase(BaseModel):
    project_id: int
    student_user_id: int
    motivation: Optional[str] = None
    status: ApplicationStatus = "PENDING"
    reviewed_by: Optional[int] = None
    reviewed_at: Optional[datetime] = None
    decision_note: Optional[str] = None


class ProjectApplicationCreate(ProjectApplicationBase):
    pass


class ProjectApplicationUpdate(BaseModel):
    motivation: Optional[str] = None
    status: Optional[ApplicationStatus] = None
    reviewed_by: Optional[int] = None
    reviewed_at: Optional[datetime] = None
    decision_note: Optional[str] = None


class ProjectApplicationResponse(ProjectApplicationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: Optional[datetime] = None

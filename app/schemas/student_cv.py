from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict


StudentLevel = Literal["PHD", "UNDERGRADUATE", "GRADUATE"]


class StudentCVBase(BaseModel):
    title: str
    university: Optional[str] = None
    level: Optional[StudentLevel] = None
    major: Optional[str] = None
    bio: Optional[str] = None
    experience: Optional[str] = None
    research_interests: Optional[str] = None
    skills: Optional[str] = None
    cv_url: Optional[str] = None


class StudentCVCreate(StudentCVBase):
    student_user_id: int


class StudentCVUpdate(BaseModel):
    title: Optional[str] = None
    university: Optional[str] = None
    level: Optional[StudentLevel] = None
    major: Optional[str] = None
    bio: Optional[str] = None
    experience: Optional[str] = None
    research_interests: Optional[str] = None
    skills: Optional[str] = None
    cv_url: Optional[str] = None


class StudentCVResponse(StudentCVBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_user_id: int
    created_at: Optional[datetime] = None

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict


TeacherGrade = Literal["MCA", "PROFESSOR", "DOCTOR", "ADMIN"]


class TeacherBase(BaseModel):
    experience_years: int = 0
    grade: Optional[TeacherGrade] = None
    department: Optional[str] = None
    research_interests: Optional[str] = None


class TeacherCreate(TeacherBase):
    user_id: int


class TeacherUpdate(BaseModel):
    experience_years: Optional[int] = None
    grade: Optional[TeacherGrade] = None
    department: Optional[str] = None
    research_interests: Optional[str] = None


class TeacherResponse(TeacherBase):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    created_at: Optional[datetime] = None

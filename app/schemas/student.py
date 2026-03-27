from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict

class StudentBase(BaseModel):
    university: Optional[str] = None
    level: Optional[Literal["PHD", "UNDERGRADUATE", "GRADUATE"]] = None
    major: Optional[str] = None
    bio: Optional[str] = None
    experience: Optional[str] = None
    research_interests: Optional[str] = None
    skills: Optional[str] = None
    cv_url: Optional[str] = None


class StudentCreate(StudentBase):
    user_id: int


class StudentUpdate(BaseModel):
    university: Optional[str] = None
    level: Optional[Literal["PHD", "UNDERGRADUATE", "GRADUATE"]] = None
    major: Optional[str] = None
    bio: Optional[str] = None
    experience: Optional[str] = None
    research_interests: Optional[str] = None
    skills: Optional[str] = None
    cv_url: Optional[str] = None


class StudentResponse(StudentBase):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    created_at: Optional[datetime] = None

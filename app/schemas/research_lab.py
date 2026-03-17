from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ResearchLabBase(BaseModel):
    name: str
    description: Optional[str] = None
    head_teacher_id: Optional[int] = None


class ResearchLabCreate(ResearchLabBase):
    pass


class ResearchLabUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    head_teacher_id: Optional[int] = None


class ResearchLabResponse(ResearchLabBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: Optional[datetime] = None

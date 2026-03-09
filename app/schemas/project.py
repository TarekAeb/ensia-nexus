from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict


ProjectVisibility = Literal["PUBLIC", "PRIVATE"]


class ProjectBase(BaseModel):
    group_id: int
    title: str
    description: Optional[str] = None
    visibility: ProjectVisibility = "PRIVATE"
    created_by: Optional[int] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    visibility: Optional[ProjectVisibility] = None


class ProjectResponse(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: Optional[datetime] = None

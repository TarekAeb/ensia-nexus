from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict


ResourceType = Literal["PAPER_DOC", "GIT_REPO", "DATASET", "OTHER"]


class ProjectResourceBase(BaseModel):
    project_id: int
    resource_type: ResourceType
    title: str
    url: Optional[str] = None
    created_by: Optional[int] = None


class ProjectResourceCreate(ProjectResourceBase):
    pass


class ProjectResourceUpdate(BaseModel):
    resource_type: Optional[ResourceType] = None
    title: Optional[str] = None
    url: Optional[str] = None


class ProjectResourceResponse(ProjectResourceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: Optional[datetime] = None

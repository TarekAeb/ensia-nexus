from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ResearchGroupBase(BaseModel):
    lab_id: int
    name: str
    description: Optional[str] = None
    leader_user_id: Optional[int] = None
    is_validated: bool = False
    validated_by_admin_id: Optional[int] = None
    validated_at: Optional[datetime] = None


class ResearchGroupCreate(ResearchGroupBase):
    pass


class ResearchGroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    leader_user_id: Optional[int] = None
    is_validated: Optional[bool] = None
    validated_by_admin_id: Optional[int] = None
    validated_at: Optional[datetime] = None


class ResearchGroupResponse(ResearchGroupBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: Optional[datetime] = None

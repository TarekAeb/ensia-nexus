from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class GroupMemberBase(BaseModel):
    group_id: int
    user_id: int
    is_active: bool = True


class GroupMemberCreate(GroupMemberBase):
    pass


class GroupMemberUpdate(BaseModel):
    is_active: Optional[bool] = None


class GroupMemberResponse(GroupMemberBase):
    model_config = ConfigDict(from_attributes=True)

    joined_at: Optional[datetime] = None

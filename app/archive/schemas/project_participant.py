from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict


ParticipantRole = Literal["MEMBER", "REVIEWER", "OBSERVER", "LEAD"]


class ProjectParticipantBase(BaseModel):
    project_id: int
    user_id: int
    participant_role: ParticipantRole = "MEMBER"


class ProjectParticipantCreate(ProjectParticipantBase):
    pass


class ProjectParticipantUpdate(BaseModel):
    participant_role: Optional[ParticipantRole] = None


class ProjectParticipantResponse(ProjectParticipantBase):
    model_config = ConfigDict(from_attributes=True)

    joined_at: Optional[datetime] = None

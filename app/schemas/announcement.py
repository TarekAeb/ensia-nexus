from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

class AnnouncementBase(BaseModel):
    title: str
    content: str
    category: str
    tags: Optional[str] = None
    author_user_id: int

class AnnouncementCreate(AnnouncementBase):
    pass

class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[str] = None

class AnnouncementResponse(AnnouncementBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class CommentBase(BaseModel):
    content: str
    announcement_id: int
    author_user_id: int

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class ReactionBase(BaseModel):
    announcement_id: int
    user_id: int
    reaction_type: str

class ReactionCreate(ReactionBase):
    pass

class ReactionResponse(ReactionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class InteractionSummary(BaseModel):
    comments_count: int
    reactions_count: int
    reactions_by_type: dict[str, int]
    user_reacted: Optional[str] = None # Current user's reaction type if any

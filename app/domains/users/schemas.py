from datetime import datetime

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role: str
    institution: str | None = None
    department: str | None = None
    contact_email: str | None = None
    phone_number: str | None = None
    address: str | None = None
    website: str | None = None
    email_verified: bool
    created_at: datetime


class UserUpdate(BaseModel):
    full_name: str | None = None
    contact_email: str | None = None
    phone_number: str | None = None
    address: str | None = None
    website: str | None = None

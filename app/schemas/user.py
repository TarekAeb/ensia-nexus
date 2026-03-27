from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr

UserRole = Literal["STUDENT", "TEACHER", "ADMIN", "PARTNER"]

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: UserRole
    institution: Optional[str] = None
    department: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None


class UserCreate(UserBase):
    password: Optional[str] = None


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    institution: Optional[str] = None
    department: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: Optional[datetime] = None

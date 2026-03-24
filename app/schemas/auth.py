from pydantic import BaseModel, EmailStr
from typing import Optional
from app.schemas.user import UserResponse, UserRole

class UserSignup(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role: UserRole = "STUDENT"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserPasswordChange(BaseModel):
    old_password: str
    new_password: str

class UserGoogleLogin(BaseModel):
    user_id: Optional[int] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None

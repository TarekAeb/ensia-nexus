from pydantic import BaseModel, EmailStr
from typing import Optional
from app.schemas.user import UserResponse

class UserSignup(BaseModel):
    email: EmailStr
    full_name: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserPasswordChange(BaseModel):
    old_password: str
    new_password: str

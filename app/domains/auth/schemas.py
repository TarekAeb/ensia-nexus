from pydantic import BaseModel


class UserSignup(BaseModel):
    email: str
    full_name: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class UserPasswordChange(BaseModel):
    old_password: str
    new_password: str

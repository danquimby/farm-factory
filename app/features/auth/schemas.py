from pydantic import BaseModel, EmailStr
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str | None = None


class TokenData(BaseModel):
    username: str | None = None
    user_id: int | None = None


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserRegister(UserBase):
    password: str


class UserCreate(UserBase):
    hashed_password: str | None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordReset(BaseModel):
    token: str
    new_password: str


class ChangePassword(BaseModel):
    current_password: str
    new_password: str


class RefreshTokenCreate(BaseModel):
    user_id: int
    token: str
    expires_at: datetime

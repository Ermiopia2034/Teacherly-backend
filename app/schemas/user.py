from typing import Optional
from pydantic import BaseModel, EmailStr, Field

from app.models.user import UserRole


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    role: Optional[UserRole] = UserRole.teacher


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str
    role: UserRole = UserRole.teacher


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: int
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True


# Properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB but not returned by API
class UserInDB(UserInDBBase):
    hashed_password: str

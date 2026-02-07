from typing import Optional, List

from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserUpdateSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserPublicSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    update_at: datetime


class UserListPublicSchema(BaseModel):
    users: List[UserPublicSchema]
    offset: int
    limit: int
from typing import Optional, List

from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserUpdateSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserPublicSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime


class UserListPublicSchema(BaseModel):
    users: List[UserPublicSchema]
    offset: int
    limit: int
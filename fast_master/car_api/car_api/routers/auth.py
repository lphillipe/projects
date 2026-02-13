from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from car_api.core.database import get_session
from car_api.core.security import (
    authenticate_user,
    create_access_token,
    get_current_user,
)

from car_api.models.users import User
from car_api.schemas.auth import LoginRequest, Token


router = APIRouter()
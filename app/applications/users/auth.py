from typing import Optional
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

import jwt

from app.core.database.models import User
from app.core.database.repository import UserRepository
from app.core.loader import settings


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=365)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, key=settings.AUTH_SECRET_KEY, algorithm=settings.AUTH_ALGORITHM)
    return encode_jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(login: str, password: str) -> Optional[User]:
    user: Optional[User] = await UserRepository.find_one_or_none(login=login)
    
    if not user or verify_password(plain_password=password, hashed_password=user.hashed_password) is False:
        return None
    return user
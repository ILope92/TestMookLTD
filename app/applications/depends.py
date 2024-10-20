from typing import Optional, AsyncIterator
from datetime import datetime, timezone

from fastapi import Request, HTTPException, status, Depends
from redis import asyncio as aioredis
from celery import Celery
import jwt

from app.core.base.redis import redis
from app.core.database.repository import UserRepository
from app.applications.exceptions import (
    TokenExpiredException,
    TokenNotFoundException,
    NoUserIdException,
    JwtException,
)
from app.core.loader import settings


def get_token(request: Request) -> Optional[str]:
    token: Optional[str] = request.cookies.get(settings.TOKEN_IN_COOKIES_NAME)
    if not token:
        raise TokenNotFoundException
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload: dict[str] = jwt.decode(
            jwt=token,
            key=settings.AUTH_SECRET_KEY,
            algorithms=settings.AUTH_ALGORITHM
        )
    except jwt.exceptions.PyJWTError:
        raise JwtException

    expire: str = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise TokenExpiredException

    user_id: str = payload.get('sub')
    if not user_id:
        raise NoUserIdException

    user = await UserRepository.find_one_or_none(id=int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return user

async def get_redis() -> AsyncIterator[aioredis.Redis]:
    try:
        yield redis
    finally:
        await redis.close()
        
async def get_celery_app() -> Celery:
    app = Celery(
        "tasks",
        broker=settings.CELERY_BROKER_URL,
        backend=settings.CELERY_RESULT_BACKEND,
    )

    return app

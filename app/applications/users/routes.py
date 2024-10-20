from typing import Optional

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from redis import asyncio as aioredis

from app.applications.exceptions import UserAlreadyExistsException, PasswordDontMatchException, IncorrectLoginOrPasswordException
from app.applications.users.schemas import SchemaRegister, SchemaLogin
from app.core.database.repository import UserRepository
from app.core.database.models import User
from app.applications.depends import get_redis
from app.applications.users.auth import get_password_hash, create_access_token, authenticate_user

from app.core.loader import settings


router: APIRouter = APIRouter(prefix="/user")


@router.post("/register", response_class=JSONResponse)
async def register(
    body: SchemaRegister, 
    redis: aioredis.Redis = Depends(get_redis),
):
    user = await UserRepository.find_one_or_none(login=body.login)
    if user:
        raise UserAlreadyExistsException
    if body.password_1 != body.password_2:
        raise PasswordDontMatchException
    
    hashed_password: str = get_password_hash(body.password_1)
    user: Optional[User] = await UserRepository.add(
        login=body.login,
        username=body.username,
        hashed_password=hashed_password
    )
    
    text_message: str = "Registration is successful!"
    access_token: str = create_access_token({"sub": str(user.id)})
    
    response = JSONResponse(content={'ok': True, 'access_token': access_token, 'message': text_message}, status_code=status.HTTP_201_CREATED)
    response.set_cookie(key=settings.TOKEN_IN_COOKIES_NAME, value=access_token, httponly=True)
    
    return response


@router.post("/login")
async def login(
    body: SchemaLogin,
    redis: aioredis.Redis = Depends(get_redis)
):
    user: Optional[User] = await authenticate_user(login=body.login, password=body.password)
    if user is None:
        raise IncorrectLoginOrPasswordException

    text_message: str = "Login is successful!"
    access_token: str = create_access_token({"sub": str(user.id)})
    
    response = JSONResponse(content={'ok': True, 'access_token': access_token, 'message': text_message}, status_code=status.HTTP_201_CREATED)
    response.set_cookie(key=settings.TOKEN_IN_COOKIES_NAME, value=access_token, httponly=True)
    
    return response


@router.post("/logout", response_class=JSONResponse)
async def logout_user():
    text_message: str = "The user has successfully logged out"
    
    response = JSONResponse(content={'ok': True, 'message': text_message}, status_code=status.HTTP_201_CREATED)
    response.delete_cookie(key=settings.TOKEN_IN_COOKIES_NAME)
    
    return response
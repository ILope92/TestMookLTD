from redis import asyncio as aioredis

from fastapi import APIRouter, Depends, WebSocket, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.applications.depends import get_current_user
from app.core.database.models import User
from app.core.loader import settings


router: APIRouter = APIRouter(prefix="/ws")
active_connections: dict[int, WebSocket] = {}
templates = Jinja2Templates(directory=settings.TEMPLATES_PATH)


@router.get("/", response_class=HTMLResponse, summary="Page chat")
async def get_page_chat(request: Request, user: User = Depends(get_current_user)) -> HTMLResponse:
    """Return html chat page"""
    
    return templates.TemplateResponse(
        name="chat.html", 
        context={
            "request": request,
            "user": user
        }
    )

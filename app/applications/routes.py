from fastapi import FastAPI

from app.applications.messages.routes import router as msg_router
from app.applications.users.routes import router as usr_router


def include_routes(app: FastAPI) -> FastAPI:
    app.include_router(usr_router, tags=["User"])
    app.include_router(msg_router, tags=["Message"])
    return app
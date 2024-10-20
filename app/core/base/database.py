from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.core.loader import settings


engine = create_async_engine(settings.POSTGRES_DATABASE_URL, max_overflow=-1)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() ->  AsyncIterator[AsyncSession]:
    async with async_session() as session:
        yield session
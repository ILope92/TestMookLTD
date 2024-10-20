import datetime
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, sessionmaker

from app.core.loader import settings


engine = create_async_engine(settings.POSTGRES_DATABASE_URL, max_overflow=-1)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

async def get_session() ->  AsyncIterator[AsyncSession]:
    async with async_session() as session:
        yield session

class BaseDBModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class BaseCreatedUpdatedAtModel:
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=func.now(),
        onupdate=func.current_timestamp(),
    )

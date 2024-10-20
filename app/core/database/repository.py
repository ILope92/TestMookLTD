from typing import Optional

from sqlalchemy.future import select
from sqlalchemy.sql.selectable import Select
from sqlalchemy.exc import SQLAlchemyError

from app.core.database.base import BaseDBModel
from app.core.database.models import User
from app.core.base.database import async_session


class BaseRepository:
    model = None
    
    @classmethod
    async def find_one_or_none(cls, **filter):
        async with async_session() as session:
            query: Select = select(cls.model).filter_by(**filter)
            result = await session.execute(query)
            return result.scalar_one_or_none()
    
    @classmethod
    async def find_all(cls, **filter):
        async with async_session() as session:
            query: Select = select(cls.model).filter_by(**filter)
            result = await session.execute(query)
            return result.scalars().all()
    
    @classmethod
    async def add(cls, **values):
        async with async_session() as session:
            async with session.begin():
                new_object = cls.model(**values)
                session.add(new_object)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_object
    
class UserRepository(BaseRepository):
    model = User
    
    @classmethod
    async def find_one_or_none(cls, **filter) -> Optional[User]:
        async with async_session() as session:
            query: Select = select(cls.model).filter_by(**filter)
            result = await session.execute(query)
            return result.scalar_one_or_none()
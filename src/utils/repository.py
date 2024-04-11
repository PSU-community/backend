from abc import ABC, abstractmethod
from typing import Any, Type, Unpack

from sqlalchemy import insert, select, delete

from ..database.base import BaseTable
from ..database.session import async_session_maker
from ..models.schemas.users import UserSchema


class Repository(ABC):
    @abstractmethod
    async def get_by_id(self, id: int):
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, **filter: Any):
        raise NotImplementedError

    @abstractmethod
    async def get_many(self, **filter: Any):
        raise NotImplementedError

    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def remove_by_id(self, id: int):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError


class SQLAlchemyRepository(Repository):
    table_model: Type[BaseTable] = None

    async def get_by_id(self, id: int):
        return await self.get_one(id=id)

    async def get_one(self, **filter: Unpack[table_model]) -> table_model | None:
        async with async_session_maker() as session:
            result = await session.execute(select(self.table_model).filter_by(**filter))
            data = result.scalar_one_or_none()
            return data.to_schema_model() if data else None

    async def get_many(self, **filter: Unpack[table_model]) -> list[table_model]:
        async with async_session_maker() as session:
            result = await session.execute(select(self.table_model).filter_by(**filter))
            return [table.to_schema_model() for table in result.scalars().all()]

    async def add_one(self, data: dict) -> table_model:
        async with async_session_maker() as session:
            result = await session.execute(
                insert(self.table_model).values(**data).returning(self.table_model)
            )
            await session.commit()
            return result.scalar_one().to_schema_model()

    async def remove_by_id(self, id: int):
        async with async_session_maker() as session:
            await session.execute(delete(self.table_model).filter_by(id=id))

    async def find_all(self) -> list[table_model]:
        async with async_session_maker() as session:
            result = await session.execute(
                select(self.table_model)
            )
            return [table.to_schema_model() for table in result.scalars().all()]

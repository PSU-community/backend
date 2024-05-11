from abc import ABC, abstractmethod
from typing import Any, Optional, Type, Unpack

from pydantic import BaseModel
from sqlalchemy import insert, select, delete, update
from sqlalchemy.orm import selectinload

from src.database.base import BaseTable
from src.database.session import async_session_maker
from src.utils.filters import dict_filter_none


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
    async def get_all(self):
        raise NotImplementedError

    @abstractmethod
    async def update_by_id(self, id: int, data: dict[str, Any]):
        raise NotImplementedError


class SQLAlchemyRepository(Repository):
    table_model: Type[BaseTable] = None

    async def get_by_id(self, id: int, relationship: Optional[Any] = None):
        return await self.get_one(relationship, id=id)

    async def get_one(
        self, relationship: Optional[Any] = None, **filter: Unpack[table_model]
    ) -> BaseModel | None:
        async with async_session_maker() as session:
            query = select(self.table_model).filter_by(**dict_filter_none(filter))
            if relationship is not None:
                query.options(selectinload(relationship))
            result = await session.execute(query)
            data = result.scalar_one_or_none()
            return data.to_schema_model() if data else None

    async def get_many(
        self, relationship: Optional[Any] = None, **filter: Unpack[table_model]
    ) -> list[BaseModel]:
        async with async_session_maker() as session:
            query = select(self.table_model).filter_by(**dict_filter_none(filter))
            if relationship is not None:
                query.options(selectinload(relationship))
            result = await session.execute(query)
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
            await session.commit()

    async def get_all(self, relationship: Optional[Any] = None) -> list[BaseModel]:
        async with async_session_maker() as session:
            query = select(self.table_model)
            if relationship:
                query.options(selectinload(relationship))

            result = await session.execute(query)
            return [table.to_schema_model() for table in result.scalars().all()]

    async def update_by_id(self, id: int, data: dict[str, Any]) -> BaseModel:
        async with async_session_maker() as session:
            query = (
                update(self.table_model)
                .filter_by(id=id)
                .values(**dict_filter_none(data))
                .returning(self.table_model)
            )
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one().to_schema_model()

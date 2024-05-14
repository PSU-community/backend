from typing import Any, Unpack
from pydantic import BaseModel
from sqlalchemy import desc, select
from sqlalchemy.orm import selectinload, joinedload, contains_eager

from src.utils.filters import dict_filter_none

from ..database.session import async_session_maker
from ..models.schemas.content import CategorySchema, PostSchema
from ..models.tables.tables import (
    CategoryTable,
    MediaFileTable, SubCategoryTable,
    PostTable,
    PersonalInformationTable,
)
from src.utils.abstract.db_repository import SQLAlchemyRepository


class CategoryRepository(SQLAlchemyRepository):
    table_model = CategoryTable


class SubCategoryRepository(SQLAlchemyRepository):
    table_model = SubCategoryTable

    async def get_one(self, **filter) -> BaseModel | None:
        async with async_session_maker() as session:
            query = (
                select(SubCategoryTable)
                .options(joinedload(SubCategoryTable.category))
                .filter_by(**dict_filter_none(filter))
            )

            result = await session.execute(query)
            data = result.scalar_one_or_none()
            return data.to_schema_model(load_post=False) if data else None


class PostRepository(SQLAlchemyRepository):
    table_model = PostTable


class PersonalInformationRepository(SQLAlchemyRepository):
    table_model = PersonalInformationTable


class MediaRepository(SQLAlchemyRepository):
    table_model = MediaFileTable


class ContentRepository:
    def __init__(self):
        self.category = CategoryRepository()
        self.subcategory = SubCategoryRepository()
        self.post = PostRepository()
        self.personal_information = PersonalInformationRepository()
        self.media = MediaRepository()

    async def get_popular_posts(self) -> list[PostSchema]:
        async with async_session_maker() as session:
            query = (
                select(PostTable)
                .order_by(desc(PostTable.views))
                .limit(8)
            )
            result = await session.execute(query)
            return [table.to_schema_model() for table in result.scalars().all()]

    async def get_categories(self) -> list[CategorySchema]:
        async with async_session_maker() as session:
            query = (
                select(CategoryTable) 
                .options(selectinload(CategoryTable.subcategories).joinedload(SubCategoryTable.post)) 
                .options(joinedload(CategoryTable.post))
            )

            result = await session.execute(query)
            return [table.to_schema_model() for table in result.scalars().all()]

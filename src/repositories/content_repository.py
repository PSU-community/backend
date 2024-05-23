from typing import Any, Unpack
from pydantic import BaseModel
from sqlalchemy import desc, insert, select
from sqlalchemy.orm import selectinload, joinedload

from src.utils.filters import dict_filter_none

from ..database.session import async_session_maker
from ..models.schemas.content import CategorySchema, PersonalInformationSchema, PostSchema
from ..models.tables.tables import (
    CategoryTable,
    MediaFileTable, SubCategoryTable,
    PostTable,
    PersonalInformationTable,
)
from src.utils.abstract.db_repository import SQLAlchemyRepository


class CategoryRepository(SQLAlchemyRepository):
    table_model = CategoryTable

    async def get_one(self, **filter) -> BaseModel | None:
        async with async_session_maker() as session:
            query = (
                select(CategoryTable)
                .options(joinedload(CategoryTable.post))
                .options(selectinload(CategoryTable.subcategories))
                .filter_by(**dict_filter_none(filter))
            )

            result = await session.execute(query)
            data = result.scalar_one_or_none()
            return data.to_schema_model(load_post=True, load_subcategories=True) if data else None


class SubCategoryRepository(SQLAlchemyRepository):
    table_model = SubCategoryTable

    async def get_one(self, **filter) -> BaseModel | None:
        async with async_session_maker() as session:
            query = (
                select(SubCategoryTable)
                .options(joinedload(SubCategoryTable.category))
                .options(joinedload(SubCategoryTable.post))
                .filter_by(**dict_filter_none(filter))
            )

            result = await session.execute(query)
            data = result.scalar_one_or_none()
            return data.to_schema_model(load_category=True, load_post=True) if data else None


class PostRepository(SQLAlchemyRepository):
    table_model = PostTable

    async def get_post_with_full_nested_data(self, **filter):
        async with async_session_maker() as session:
            query = (
                select(PostTable)
                .options(joinedload(PostTable.category).selectinload(CategoryTable.subcategories))
                .options(joinedload(PostTable.subcategory))
                .filter_by(**dict_filter_none(filter))
            )

            result = await session.execute(query)
            data = result.scalar_one_or_none()
            return data.to_schema_model(load_category=True, load_subcategory=True, load_category_subcategories=True) if data else None

    async def get_one(self, **filter) -> BaseModel | None:
        async with async_session_maker() as session:
            query = (
                select(PostTable)
                .options(joinedload(PostTable.category))
                .options(joinedload(PostTable.subcategory))
                .filter_by(**dict_filter_none(filter))
            )

            result = await session.execute(query)
            data = result.scalar_one_or_none()
            return data.to_schema_model(load_category=True, load_subcategory=True) if data else None

    async def add_one(self, data: dict):
        async with async_session_maker() as session:
            result = await session.execute(
                insert(PostTable)
                .values(**data)
                .returning(PostTable)
            )
            await session.commit()
            return result.scalar_one().to_schema_model()


class PersonalInformationRepository(SQLAlchemyRepository):
    table_model = PersonalInformationTable

    async def get_all(self) -> list[PersonalInformationSchema]:
        async with async_session_maker() as session:
            query = (
                select(PersonalInformationTable)
                .options(
                    joinedload(PersonalInformationTable.post)
                        .options(joinedload(PostTable.category))
                        .options(joinedload(PostTable.subcategory))
                )
            )
            response = await session.execute(query)
            return [table.to_schema_model(load_post=True, load_category=True, load_subcategory=True) for table in response.scalars().all()]
        
    async def get_many(self, **filter: Unpack[table_model]) -> list[BaseModel]:
        async with async_session_maker() as session:
            query = (
                select(PersonalInformationTable)
                .filter_by(**dict_filter_none(filter))
                .options(
                    joinedload(PersonalInformationTable.post)
                        .options(joinedload(PostTable.category))
                        .options(joinedload(PostTable.subcategory))
                )
            )
            response = await session.execute(query)
            return [table.to_schema_model(load_post=True, load_category=True, load_subcategory=True) for table in response.scalars().all()]
        
    async def get_one(self, **filter: Unpack[table_model]) -> BaseModel | None:
        async with async_session_maker() as session:
            query = (
                select(PersonalInformationTable)
                .filter_by(**dict_filter_none(filter))
                .options(
                    joinedload(PersonalInformationTable.post)
                        .options(joinedload(PostTable.category))
                        .options(joinedload(PostTable.subcategory))
                )
            )
            response = await session.execute(query)
            table = response.scalar_one_or_none()
            return table.to_schema_model(load_post=True, load_category=True, load_subcategory=True) if table else None


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
                .options(joinedload(PostTable.category))
                .options(joinedload(PostTable.subcategory))
                .order_by(desc(PostTable.views))
                .limit(8)
            )
            result = await session.execute(query)
            return [table.to_schema_model(load_category=True, load_subcategory=True) for table in result.scalars().all()]

    async def get_categories(self) -> list[CategorySchema]:
        async with async_session_maker() as session:
            query = (
                select(CategoryTable) 
                .options(selectinload(CategoryTable.subcategories).joinedload(SubCategoryTable.post)) 
                .options(joinedload(CategoryTable.post))
            )

            result = await session.execute(query)
            return [table.to_schema_model(load_subcategories=True, load_subcategories_posts=True, load_post=True) for table in result.scalars().all()]

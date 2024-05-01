from sqlalchemy import desc, select
from sqlalchemy.orm import selectinload

from ..database.session import async_session_maker
from ..models.schemas.content import PostSchema
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

    async def get_popular_categories(self) -> list[PostSchema]:
        async with async_session_maker() as session:
            query = (
                select(PostTable)
                .order_by(desc(PostTable.views))
                .limit(8)
            )
            result = await session.execute(query)
            return [table.to_schema_model() for table in result.scalars().all()]

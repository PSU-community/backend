from sqlalchemy import desc, select

from ..database.session import async_session_maker
from ..models.tables.tables import (
    CategoryTable,
    SubCategoryTable,
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


class ContentRepository:
    def __init__(self):
        self.category = CategoryRepository()
        self.subcategory = SubCategoryRepository()
        self.post = PostRepository()
        self.personal_information = PersonalInformationRepository()

    async def get_popular_categories(self):
        async with async_session_maker() as session:
            query = select(PostTable.category_id, PostTable.category_id, PostTable.views) \
                .join(CategoryTable, PostTable.category_id == CategoryTable.id) \
                .join(SubCategoryTable, PostTable.subcategory_id == SubCategoryTable.id) \
                .order_by(desc(PostTable.views)) \
                .limit(8)
            result = await session.execute(query)
            return result.all()

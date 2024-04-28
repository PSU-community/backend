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

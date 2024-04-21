from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects import postgresql

from src.database.base import BaseTable, int_pk, str_128
from src.models.enums import MediaTypes, PersonalInformationTypes
from src.models.schemas.content import (
    CategorySchema,
    SubCategorySchema,
    PostSchema,
    PersonalInformationSchema, UploadedFileSchema,
)
from src.models.tables.users import UserTable


class CategoryTable(BaseTable):
    __tablename__ = "categories"

    id: Mapped[int_pk]
    name: Mapped[str_128]

    subcategories: Mapped[list["SubCategoryTable"]] = relationship()

    def to_schema_model(self):
        return CategorySchema(
            id=self.id,
            name=self.name,
        )


class SubCategoryTable(BaseTable):
    __tablename__ = "subcategories"

    id: Mapped[int_pk]
    # Игнор при удалении в случае случайного удаления администратором
    section_id: Mapped[int] = mapped_column(ForeignKey(CategoryTable.id))
    name: Mapped[str_128]

    category: Mapped["CategoryTable"] = relationship()
    # contents: Mapped[list["PostTable"]] = relationship()

    def to_schema_model(self):
        return SubCategorySchema(
            id=self.id,
            section_id=self.section_id,
            name=self.name,
        )


class PostTable(BaseTable):
    __tablename__ = "posts"

    id: Mapped[int_pk]
    # При удалении разделы или темы, сам контент остаётся.
    # Сделано это в случае случайного удаления.
    section_id: Mapped[int] = mapped_column(ForeignKey(CategoryTable.id))
    section_theme_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(SubCategoryTable.id)
    )
    content: str

    category: Mapped["CategoryTable"] = relationship()
    subcategory: Mapped["SubCategoryTable"] = relationship()

    def to_schema_model(self):
        return PostSchema(
            id=self.id,
            section_id=self.section_id,
            section_theme_id=self.section_theme_id,
            content=self.content,
        )


class UploadedFileTable(BaseTable):
    __tablename__ = "uploaded_files"
    id: Mapped[int_pk]
    name: Mapped[str_128]
    url: Mapped[str_128]
    type: Mapped[int]

    def to_schema_model(self):
        return UploadedFileSchema(
            id=self.id,
            name=self.name,
            url=self.url,
            type=MediaTypes(self.type),
        )


class PersonalInformationTable(BaseTable):
    __tablename__ = "personal_information"

    id: Mapped[int_pk]
    informational_content_id: Mapped[int] = mapped_column(
        ForeignKey(PostTable.id)
    )
    user_id: Mapped[int] = mapped_column(ForeignKey(UserTable.id))
    content_type: Mapped[PersonalInformationTypes] = mapped_column(postgresql.ENUM(PersonalInformationTypes))
    content: Mapped[Optional[str]]

    def to_schema_model(self):
        return PersonalInformationSchema(
            id=self.id,
            informational_content_id=self.informational_content_id,
            user_id=self.user_id,
            content_type=self.content_type,
            content=self.content,
        )

from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import BaseTable, int_pk, str_128
from src.models.enums import ContentTypes, PersonalInformationTypes
from src.models.schemas.users import UserSchema
from src.models.schemas.informational_contents import SectionSchema, SectionThemeSchema, InformationalContentSchema, PersonalInformationSchema


class UserTable(BaseTable):
    __tablename__ = "users"

    id: Mapped[int_pk]
    name: Mapped[str_128]
    email: Mapped[str_128]
    hashed_password: Mapped[bytes]
    permissions: Mapped[int]  # TODO: int flag

    def to_schema_model(self):
        return UserSchema(
            id=self.id,
            name=self.name,
            email=self.email,
            hashed_password=self.hashed_password,
            permissions=self.permissions,
        )


class SectionTable(BaseTable):
    __tablename__ = "sections"

    id: Mapped[int_pk]
    name: Mapped[str_128]

    def to_schema_model(self):
        return SectionSchema(
            id=self.id,
            name=self.name,
        )


class SectionThemesTable(BaseTable):
    __tablename__ = "section_themes"

    id: Mapped[int_pk]
    section_id: Mapped[int] = mapped_column(ForeignKey(SectionTable.id))
    name: Mapped[str_128]

    def to_schema_model(self):
        return SectionThemeSchema(
            id=self.id,
            section_id=self.section_id,
            name=self.name,
        )


class InformationalContentTable(BaseTable):
    __tablename__ = "informational_contents"

    id: Mapped[int_pk]
    section_id: Mapped[int] = mapped_column(ForeignKey(SectionTable.id))
    section_theme_id: Mapped[int] = mapped_column(ForeignKey(SectionThemesTable.id))
    name: Mapped[str_128]
    file_url: Mapped[Optional[str_128]]
    content: Mapped[Optional[str]]
    content_type: Mapped[ContentTypes]

    def to_schema_model(self):
        return InformationalContentSchema(
            id=self.id,
            section_id=self.section_id,
            section_theme_id=self.section_theme_id,
            name=self.name,
            file_url=self.file_url,
            content=self.content,
            content_type=self.content_type,
        )


class PersonalInformationTable(BaseTable):
    __tablename__ = "personal_information"

    id: Mapped[int_pk]
    informational_content_id: Mapped[int] = mapped_column(ForeignKey(InformationalContentTable.id))
    user_id: Mapped[int] = mapped_column(ForeignKey(UserTable.id))
    content_type: Mapped[PersonalInformationTypes]
    content: Mapped[Optional[str]]

    def to_schema_model(self):
        return PersonalInformationSchema(
            id=self.id,
            informational_content_id=self.informational_content_id,
            user_id=self.user_id,
            content_type=self.content_type,
            content=self.content,
        )

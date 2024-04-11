from typing import Optional

from pydantic import BaseModel

from ..enums import ContentTypes, PersonalInformationTypes


class IdSchema(BaseModel):
    id: int


class SectionCreate(BaseModel):
    name: str


class SectionSchema(IdSchema, SectionCreate):
    ...


class SectionThemeCreate(BaseModel):
    section_id: int
    name: str


class SectionThemeSchema(IdSchema, SectionThemeCreate):
    ...


class InformationalContentCreate(BaseModel):
    section_id: int
    section_theme_id: int
    name: str
    content: Optional[str]
    content_type: ContentTypes


class InformationalContentSchema(IdSchema, InformationalContentCreate):
    file_url: Optional[str]


class PersonalInformationCreate(BaseModel):
    informational_content_id: int
    user_id: int
    content_type: PersonalInformationTypes
    content: Optional[str]


class PersonalInformationSchema(IdSchema, PersonalInformationCreate):
    ...

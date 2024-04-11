from typing import Optional

from pydantic import BaseModel

from ..enums import ContentTypes, PersonalInformationTypes


class IdSchema(BaseModel):
    id: int


class SectionAddSchema(BaseModel):
    name: str


class SectionSchema(IdSchema, SectionAddSchema):
    ...


class SectionThemeAddSchema(BaseModel):
    section_id: int
    name: str


class SectionThemeSchema(IdSchema, SectionThemeAddSchema):
    ...


class InformationalContentAddSchema(BaseModel):
    section_id: int
    section_theme_id: int
    name: str
    file_url: Optional[str]
    content: Optional[str]
    content_type: ContentTypes


class InformationalContentSchema(IdSchema, InformationalContentAddSchema):
    ...


class PersonalInformationAddSchema(BaseModel):
    informational_content_id: int
    user_id: int
    content_type: PersonalInformationTypes
    content: Optional[str]


class PersonalInformationSchema(IdSchema, PersonalInformationAddSchema):
    ...

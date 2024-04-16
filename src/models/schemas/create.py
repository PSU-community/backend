from typing import Optional

from pydantic import BaseModel

from src.models.enums import ContentTypes, PersonalInformationTypes


class SectionCreate(BaseModel):
    name: str


class SectionThemeCreate(BaseModel):
    section_id: int
    name: str


class InformationalContentCreate(BaseModel):
    section_id: int
    section_theme_id: Optional[int]
    name: str
    content_type: ContentTypes


class PersonalInformationCreate(BaseModel):
    informational_content_id: int
    user_id: int
    content_type: PersonalInformationTypes
    content: Optional[str]

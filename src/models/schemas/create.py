from typing import Optional

from pydantic import BaseModel

from src.models.enums import ContentTypes, PersonalInformationTypes


class CategoryCreate(BaseModel):
    name: str


class SubCategoryCreate(BaseModel):
    section_id: int
    name: str


class PostCreate(BaseModel):
    section_id: int
    section_theme_id: Optional[int]
    content: str


class PersonalInformationCreate(BaseModel):
    informational_content_id: int
    user_id: int
    content_type: PersonalInformationTypes
    content: Optional[str]

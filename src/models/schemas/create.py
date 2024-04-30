from typing import Optional

from pydantic import BaseModel, Field

from src.models.enums import ContentTypes, MediaTypes, PersonalInformationTypes


class CategoryCreate(BaseModel):
    name: str
    subcategories: list[str]


class SubCategoryCreate(BaseModel):
    category_id: int
    name: str


class PostCreate(BaseModel):
    category_id: int
    subcategory_id: Optional[int]
    content: str


class PersonalInformationCreate(BaseModel):
    informational_content_id: int
    user_id: int
    content_type: PersonalInformationTypes
    content: Optional[str]


class RequestMediaSchema(BaseModel):
    name: str
    type: MediaTypes
    json: str


class CreateMediaSchema(RequestMediaSchema):
    url: Optional[str] = Field(defalt=None)


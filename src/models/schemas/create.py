from typing import Optional, Any

from pydantic import BaseModel, Field

from src.models.enums import MediaTypes, PersonalInformationTypes


class CategoryCreate(BaseModel):
    name: str
    subcategories: list[str]


class SubCategoryCreate(BaseModel):
    category_id: int
    name: str


class PostCreate(BaseModel):
    category_id: Optional[int] = Field(default=None)
    subcategory_id: Optional[int] = Field(default=None)
    content: Optional[str] = Field(default=None)


class PersonalInformationCreate(BaseModel):
    post_id: int
    content_type: PersonalInformationTypes
    content: Optional[str] = Field(default=None)


class RequestMediaSchema(BaseModel):
    file_name: Optional[str] = Field(default=None)
    type: MediaTypes
    data: Optional[Any] = Field(default=None)


class CreateMediaSchema(RequestMediaSchema):
    file_url: Optional[str] = Field(default=None)


class GuideCreate(BaseModel):
    name: str
    content: str

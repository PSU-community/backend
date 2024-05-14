from typing import Optional

from pydantic import Field

from .base import IdSchema
from .create import (
    PostCreate,
    PersonalInformationCreate,
)
from ..enums import MediaTypes


class SubCategorySchema(IdSchema):
    category_id: int
    name: str
    category: Optional["CategorySchema"] = Field(default=None)
    post: Optional["PostSchema"] = Field(default=None)


class CategorySchema(IdSchema):
    name: str
    subcategories: Optional[list[SubCategorySchema]] = Field(default=None)
    post: Optional["PostSchema"] = Field(default=None)


class PostSchema(IdSchema, PostCreate):
    views: Optional[int] = Field(default=None)
    category: Optional[CategorySchema] = Field(default=None)
    subcategory: Optional[SubCategorySchema] = Field(default=None)


class PersonalInformationSchema(IdSchema, PersonalInformationCreate):
    ...


class MediaFileSchema(IdSchema):
    file_name: Optional[str] = Field(default=None)
    file_url: Optional[str] = Field(default=None)
    type: MediaTypes
    data: Optional[str] = Field(default=None)

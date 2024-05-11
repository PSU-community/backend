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


class CategorySchema(IdSchema):
    name: str
    subcategories: Optional[list[SubCategorySchema]] = None


class PostSchema(IdSchema, PostCreate):
    views: int
    category: CategorySchema
    subcategory: Optional[SubCategorySchema] = Field(default=None)


class PersonalInformationSchema(IdSchema, PersonalInformationCreate):
    ...


class MediaFileSchema(IdSchema):
    file_name: Optional[str] = Field(default=None)
    file_url: Optional[str] = Field(default=None)
    type: MediaTypes
    data: Optional[str] = Field(default=None)

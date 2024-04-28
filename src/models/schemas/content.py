from typing import Optional

from .base import IdSchema
from .create import (
    PostCreate,
    PersonalInformationCreate,
    CategoryCreate,
    SubCategoryCreate,
)
from ..enums import MediaTypes


class CategorySchema(IdSchema):
    name: str


class SubCategorySchema(IdSchema):
    category_id: int
    name: str


class PostSchema(IdSchema, PostCreate):
    views: int


class PersonalInformationSchema(IdSchema, PersonalInformationCreate): ...


class UploadedFileSchema(IdSchema):
    name: str
    url: str
    type: MediaTypes

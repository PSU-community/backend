from typing import Optional

from .base import IdSchema
from .create import (
    PostCreate,
    PersonalInformationCreate,
    CategoryCreate,
    SubCategoryCreate,
)
from ..enums import MediaTypes


class CategorySchema(IdSchema, CategoryCreate):
    themes: list["SubCategorySchema"]


class SubCategorySchema(IdSchema, SubCategoryCreate): ...


class PostSchema(IdSchema, PostCreate):
    ...


class PersonalInformationSchema(IdSchema, PersonalInformationCreate):
    ...


class UploadedFileSchema(IdSchema):
    name: str
    url: str
    type: MediaTypes

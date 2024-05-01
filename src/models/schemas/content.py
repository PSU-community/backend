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
    name: str
    url: str
    type: MediaTypes
    data: str

# Закладки (или заметка) к выделененному фрагменту текста
# Парсинг docx
# Возможность вставить текстовый документ и ворд и внести как текст

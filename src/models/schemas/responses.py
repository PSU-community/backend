from typing import Optional

from pydantic import BaseModel, Field

from src.models.schemas.content import CategorySchema, SubCategorySchema


class PostResponseSchema(BaseModel):
    id: int
    category_id: int
    subcategory_id: Optional[int] = Field(default=None)


class SubcategoryResponseSchema(BaseModel):
    id: int
    category_id: int
    name: str
    post: Optional[PostResponseSchema] = Field(default=None)


class CategoryResponseSchema(BaseModel):
    id: int
    name: str
    subcategories: Optional[list[SubcategoryResponseSchema]] = Field(default=None)
    post: Optional[PostResponseSchema] = Field(default=None)


class PopularPostSchema(BaseModel):
    id: int
    category_id: int
    subcategory_id: Optional[int] = Field(default=None)
    views: int
    category: CategorySchema
    subcategory: Optional[SubCategorySchema] = Field(default=None)

from typing import Optional

from pydantic import BaseModel, Field


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
    subcategories: list[SubcategoryResponseSchema]
    post: Optional[PostResponseSchema] = Field(default=None)
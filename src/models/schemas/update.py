from typing import Optional, Any

from pydantic import BaseModel, Field

from src.models.enums import UserPermissions


class CategoryUpdate(BaseModel):
    name: str


class SubCategoryUpdate(BaseModel):
    category_id: int
    name: str


class PostUpdate(BaseModel):
    content: str


class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    password: Optional[str] = Field(default=None)
    is_verified: Optional[bool] = Field(default=None)
    permissions: Optional[UserPermissions] = Field(default=None)


class MediaUpdate(BaseModel):
    # TODO: overhaul
    data: Any

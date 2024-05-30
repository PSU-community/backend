from typing import Optional, Any

from pydantic import BaseModel, Field

from src.models.enums import UserPermissions
from src.models.schemas.tests import TestQuestion, TestResult


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
    hashed_password: Optional[bytes] = Field(default=None)
    is_verified: Optional[bool] = Field(default=None)
    permissions: Optional[UserPermissions] = Field(default=None)


class MediaUpdate(BaseModel):
    # TODO: overhaul
    data: Any


class UserContentUpdate(BaseModel):
    content: str


class GuideUpdate(BaseModel):
    content: str


class TestUpdate(BaseModel):
    name: str
    questions: list[TestQuestion]
    results: list[TestResult]

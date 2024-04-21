from typing import Optional, overload

from src.models.schemas.content import (
    CategorySchema,
    SubCategorySchema,
    PostSchema,
)
from src.models.schemas.create import (
    PostCreate,
    CategoryCreate,
    SubCategoryCreate,
)
from src.models.schemas.update import SectionThemeUpdate, SectionUpdate
from src.models.tables.tables import CategoryTable
from src.repositories.content_repository import ContentRepository
from src.repositories.meili_search_repository import MeiliSearchRepository


class ContentService:
    def __init__(self):
        self.repository = ContentRepository()
        self.search = MeiliSearchRepository

    async def get_category(
        self, category_id: int, with_subcategories: bool = True
    ) -> CategorySchema:
        return await self.repository.category.get_by_id(
            category_id, relationship=CategoryTable.subcategories if with_subcategories else None
        )

    async def get_category_list(self, with_subcategories: bool = True) -> list[CategorySchema]:
        return await self.repository.category.get_all(
            relationship=CategoryTable.subcategories if with_subcategories else None
        )

    async def add_category(self, category_create: CategoryCreate):
        await self.repository.category.add_one(category_create.model_dump())

    async def update_category(self, category_id: int, category_update: SectionUpdate):
        return await self.repository.category.update_by_id(
            category_id, category_update.model_dump(exclude_none=True)
        )

    async def delete_category(self, category_id: int):
        return await self.repository.category.remove_by_id(category_id)

    async def get_subcategory(self, subcategory_id: int) -> SubCategorySchema:
        return await self.repository.subcategory.get_by_id(subcategory_id)

    async def add_subcategory(
        self, subcategory_create: SubCategoryCreate
    ) -> SubCategorySchema:
        return await self.repository.subcategory.add_one(
            subcategory_create.model_dump()
        )

    async def update_subcategory(
        self, theme_id: int, theme_update: SectionThemeUpdate
    ) -> SubCategorySchema:
        return await self.repository.subcategory.update_by_id(
            theme_id, theme_update.model_dump(exclude_none=True)
        )

    async def delete_subcategory(self, theme_id: int):
        return await self.repository.subcategory.remove_by_id(theme_id)

    async def get_post_list(
        self, *, category_id: int, theme_id: Optional[int] = None
    ) -> list[PostSchema]:
        return await self.repository.post.get_many(
            category_id=category_id, subcategory_id=theme_id
        )

    async def add_post(self, post_create: PostCreate):
        await self.repository.post.add_one(post_create.model_dump())

    @overload
    def search(self, query: str, /): ...

    @overload
    def search(self, query: str, /, post_ids: list[int]): ...

    def search(self, query: str, /, post_id: int = None):
        if post_id is None:
            return self.search.search(query)
        return self.search.search_in_documents([post_id], query)

from typing import Optional, overload

from src.models.schemas.informational_contents import (
    SectionSchema,
    SectionThemeSchema,
    InformationalContentSchema,
)
from src.models.schemas.create import (
    InformationalContentCreate,
    SectionCreate,
    SectionThemeCreate,
)
from src.models.schemas.update import SectionThemeUpdate, SectionUpdate
from src.models.tables.tables import SectionTable
from src.repositories.content_repository import ContentRepository
from src.repositories.meili_search_repository import MeiliSearchRepository


class ContentService:
    def __init__(self):
        self.repository = ContentRepository()
        self.search = MeiliSearchRepository

    async def get_section(
        self, section_id: int, with_themes: bool = True
    ) -> SectionSchema:
        return await self.repository.section.get_by_id(
            section_id, relationship=SectionTable.themes if with_themes else None
        )

    async def get_section_list(self, with_themes: bool = True) -> list[SectionSchema]:
        return await self.repository.section.get_all(
            relationship=SectionTable.themes if with_themes else None
        )

    async def add_section(self, section_create: SectionCreate):
        await self.repository.section.add_one(section_create.model_dump())

    async def update_section(self, section_id: int, section_update: SectionUpdate):
        return await self.repository.section.update_by_id(
            section_id, section_update.model_dump(exclude_none=True)
        )

    async def delete_section(self, section_id: int):
        return await self.repository.section.remove_by_id(section_id)

    async def get_section_theme(self, section_theme_id: int) -> SectionThemeSchema:
        return await self.repository.section_theme.get_by_id(section_theme_id)

    async def add_section_theme(
        self, section_theme_create: SectionThemeCreate
    ) -> SectionThemeSchema:
        return await self.repository.section_theme.add_one(
            section_theme_create.model_dump()
        )

    async def update_section_theme(
        self, theme_id: int, theme_update: SectionThemeUpdate
    ) -> SectionThemeSchema:
        return await self.repository.section_theme.update_by_id(
            theme_id, theme_update.model_dump(exclude_none=True)
        )

    async def delete_section_theme(self, theme_id: int):
        return await self.repository.section_theme.remove_by_id(theme_id)

    async def get_content_list(
        self, *, section_id: int, theme_id: Optional[int] = None
    ) -> list[InformationalContentSchema]:
        return await self.repository.informational_content.get_many(
            section_id=section_id, section_theme_id=theme_id
        )

    async def add_content(self, content_create: InformationalContentCreate):
        await self.repository.informational_content.add_one(content_create.model_dump())

    @overload
    def search(self, query: str, /): ...

    @overload
    def search(self, query: str, /, content_ids: list[int]): ...

    def search(self, query: str, /, content_ids: list[int] = None):
        if content_ids is None:
            return self.search.search(query)
        return self.search.search_in_documents(content_ids, query)

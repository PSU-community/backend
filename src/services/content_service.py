from typing import Optional

from src.models.schemas.informational_contents import SectionSchema, SectionCreate, SectionThemeSchema, SectionThemeCreate, InformationalContentSchema, InformationalContentCreate
from src.repositories.content_repository import ContentRepository


class ContentService:
    def __init__(self):
        self.repository = ContentRepository()

    async def get_section(self, section_id: int) -> SectionSchema:
        return await self.repository.section.get_by_id(section_id)

    async def get_section_list(self) -> list[SectionSchema]:
        return await self.repository.section.find_all()

    async def add_section(self, section_create: SectionCreate):
        await self.repository.section.add_one(section_create.model_dump())

    async def get_section_theme(self, section_theme_id: int) -> SectionThemeSchema:
        return await self.repository.section_theme.get_by_id(section_theme_id)

    async def add_section_theme(self, section_theme_create: SectionThemeCreate):
        await self.repository.section_theme.add_one(section_theme_create.model_dump())

    async def get_content_list(self, *, section_id: int, theme_id: Optional[int] = None) -> list[InformationalContentSchema]:
        return await self.repository.informational_content.get_many(section_id=section_id, section_theme_id=theme_id)

    async def add_content(self, content_create: InformationalContentCreate):
        await self.repository.informational_content.add_one(content_create.model_dump())


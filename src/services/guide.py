from src.models.schemas.create import GuideCreate
from src.models.schemas.guide import GuideSchema
from src.models.schemas.update import GuideUpdate
from src.repositories.guide import GuideRepository


class GuideService:
    def __init__(self) -> None:
        self.repository = GuideRepository()

    async def get_guide_list(self) -> list[GuideSchema]:
        return await self.repository.get_all()
    
    async def get_guide_by_id(self, id: int) -> GuideSchema:
        return await self.repository.get_by_id(id)

    async def add_guide(self, create: GuideCreate):
        await self.repository.add_one(create.model_dump())

    async def update_guide(self, id: int, update: GuideUpdate):
        await self.repository.update_by_id(id, update.model_dump())

    async def delete_guide(self, id: int):
        await self.repository.remove_by_id(id)

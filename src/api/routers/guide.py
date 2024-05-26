from fastapi import APIRouter

from src.api.dependencies import GuideServiceDep, IAdminUser
from src.models.schemas.create import GuideCreate
from src.models.schemas.guide import GuideSchema
from src.models.schemas.update import GuideUpdate

router = APIRouter(tags=["Инструкции"])


@router.get("/guide/list")
async def get_guide_list(user: IAdminUser, service: GuideServiceDep) -> list[GuideSchema]:
    return await service.get_guide_list()


@router.get("/guide/{guide_id}")
async def get_guide_by_id(guide_id: int, user: IAdminUser, service: GuideServiceDep) -> GuideSchema:
    return await service.get_guide_by_id(guide_id)


@router.post("/guide")
async def add_guide(guide_create: GuideCreate, user: IAdminUser, service: GuideServiceDep):
    await service.add_guide(guide_create)


@router.patch("/guide/{guide_id}")
async def update_guide(guide_id: int, guide_update: GuideUpdate, user: IAdminUser, service: GuideServiceDep):
    await service.update_guide(guide_id, guide_update)


@router.delete("/guide/{guide_id}")
async def delete_guide(guide_id: int, user: IAdminUser, service: GuideServiceDep):
    await service.delete_guide(guide_id)
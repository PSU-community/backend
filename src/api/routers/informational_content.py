from fastapi import APIRouter, HTTPException
from starlette import status

from src.api.dependencies import IAdminUser, IContentService
from src.models.schemas.create import SectionCreate, SectionThemeCreate
from src.models.schemas.informational_contents import (
    InformationalContentSchema,
    SectionSchema,
    SectionThemeSchema,
)
from src.models.schemas.update import SectionThemeUpdate, SectionUpdate

router = APIRouter(tags=["Informational content"])


@router.get("/sections")
async def get_section_list(service: IContentService) -> list[SectionSchema]:
    return await service.get_section_list(with_themes=True)


@router.post("/sections")
async def add_section(
    section_create: SectionCreate, service: IContentService, user: IAdminUser
):
    return await service.add_section(section_create)


@router.get("/sections/{section_id}")
async def get_section(section_id: int, service: IContentService) -> SectionSchema:
    section = await service.get_section(section_id, with_themes=True)
    if section is not None:
        return section

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Section with this id was not found",
    )


@router.patch("/sections/{section_id}")
async def update_section(
    section_id: int,
    section_update: SectionUpdate,
    service: IContentService,
    user: IAdminUser,
):
    section = await service.update_section(section_id, section_update)
    if section is not None:
        return section

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Section with this id was not found",
    )


@router.delete("/sections/{section_id}")
async def delete_section(section_id: int, service: IContentService, user: IAdminUser):
    return await service.delete_section(section_id)


@router.get("/sections/{section_id}/content")
async def get_section_content(
    section_id: int, service: IContentService
) -> list[InformationalContentSchema]:
    content = await service.get_content_list(section_id=section_id)

    if content:
        return content

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Section with this id was not found",
    )


@router.post("/themes")
async def add_section_theme(
    theme_create: SectionThemeCreate, service: IContentService, user: IAdminUser
) -> SectionThemeSchema:
    return await service.add_section_theme(theme_create)


@router.patch("/themes/{theme_id}")
async def update_section_theme(
    theme_id: int,
    theme_update: SectionThemeUpdate,
    service: IContentService,
    user: IAdminUser,
) -> SectionThemeSchema:
    return await service.update_section_theme(theme_id, theme_update)


@router.delete("/themes/{theme_id}")
async def delete_section_theme(
    theme_id: int, service: IContentService, user: IAdminUser
):
    return await service.delete_section_theme(theme_id)

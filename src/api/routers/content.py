from fastapi import APIRouter, HTTPException
from starlette import status

from src.api.dependencies import IAdminUser, IContentService
from src.models.schemas.create import CategoryCreate, SubCategoryCreate
from src.models.schemas.content import (
    PostSchema,
    CategorySchema,
    SubCategorySchema,
)
from src.models.schemas.update import SectionThemeUpdate, SectionUpdate

router = APIRouter(tags=["Informational content"])


@router.get("/categories")
async def get_category_list(service: IContentService) -> list[CategorySchema]:
    return await service.get_category_list(with_subcategories=True)


@router.post("/categories")
async def add_category(
    category_create: CategoryCreate, service: IContentService, user: IAdminUser
):
    return await service.add_category(category_create)


@router.get("/categories/{category_id}")
async def get_category(category_id: int, service: IContentService) -> CategorySchema:
    category = await service.get_category(category_id, with_subcategories=True)
    if category is not None:
        return category

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Section with this id was not found",
    )


@router.patch("/categories/{category_id}")
async def update_category(
    category_id: int,
    category_update: SectionUpdate,
    service: IContentService,
    user: IAdminUser,
):
    category = await service.update_category(category_id, category_update)
    if category is not None:
        return category

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Section with this id was not found",
    )


@router.delete("/categories/{category_id}")
async def delete_category(category_id: int, service: IContentService, user: IAdminUser):
    return await service.delete_category(category_id)


@router.get("/categories/{category_id}/content")
async def get_category_content(
    category_id: int, service: IContentService
) -> list[PostSchema]:
    content = await service.get_content_list(category_id=category_id)

    if content:
        return content

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Section with this id was not found",
    )


@router.post("/subcategories")
async def add_category_theme(
    theme_create: SubCategoryCreate, service: IContentService, user: IAdminUser
) -> SubCategorySchema:
    return await service.add_category_theme(theme_create)


@router.patch("/subcategories/{subcategory_id}")
async def update_category_theme(
    subcategory_id: int,
    theme_update: SectionThemeUpdate,
    service: IContentService,
    user: IAdminUser,
) -> SubCategorySchema:
    return await service.update_category_theme(subcategory_id, theme_update)


@router.delete("/subcategories/{subcategory_id}")
async def delete_category_theme(
    subcategory_id: int, service: IContentService, user: IAdminUser
):
    return await service.delete_subcategory(subcategory_id)

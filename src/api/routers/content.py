from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from starlette import status

from src.api.dependencies import IAdminUser, IContentService
from src.models.schemas.create import CategoryCreate, PostCreate, SubCategoryCreate
from src.models.schemas.content import (
    PostSchema,
    CategorySchema,
    SubCategorySchema,
)
from src.models.schemas.update import SubCategoryUpdate, CategoryUpdate

router = APIRouter(
    tags=["Informational content"], dependencies=[Depends(HTTPBearer(auto_error=False))]
)


@router.get("/popular")
async def get_popular_categories(service: IContentService):
    return await service.get_popular_categories()


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
    category_update: CategoryUpdate,
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


@router.post("/subcategories")
async def add_category_subcategory(
    subcategory_create: SubCategoryCreate, service: IContentService, user: IAdminUser
) -> SubCategorySchema:
    return await service.add_subcategory(subcategory_create)


@router.patch("/subcategories/{subcategory_id}")
async def update_subcategory(
    subcategory_id: int,
    subcategory_update: SubCategoryUpdate,
    service: IContentService,
    user: IAdminUser,
) -> SubCategorySchema:
    return await service.update_subcategory(subcategory_id, subcategory_update)


@router.delete("/subcategories/{subcategory_id}")
async def delete_subcategory(
    subcategory_id: int, service: IContentService, user: IAdminUser
):
    return await service.delete_subcategory(subcategory_id)


@router.get("/posts")
async def get_posts(service: IContentService):
    return await service.get_post()

@router.get("/posts/{post_id}")
async def get_post(post_id: int, service: IContentService) -> PostSchema:
    return await service.get_post(post_id)


@router.post("/posts")
async def add_post(post_create: PostCreate, service: IContentService, user: IAdminUser):
    return await service.add_post(post_create)

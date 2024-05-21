from typing import Optional
from fastapi import APIRouter

from src.api import exceptions
from src.models.enums import PersonalInformationTypes
from src.models.schemas.create import PersonalInformationCreate
from src.models.schemas.update import UserContentUpdate

from ...api.dependencies import IContentService, ICurrentUser

router = APIRouter(tags=["Пользователи::Персональная информация"])


@router.get("/me/content")
async def get_user_content_list(
    user: ICurrentUser, 
    content_service: IContentService,
    type: Optional[PersonalInformationTypes] = None,
    post_id: Optional[int] = None,
    ):
    if type is not None:
        return await content_service.get_user_content_list_by_type(user.id, type)
    elif post_id is not None:
        return await content_service.get_user_content_list_by_post(user.id, post_id)


@router.post("/me/content")
async def add_user_content(content_create: PersonalInformationCreate, user: ICurrentUser, content_service: IContentService):
    await content_service.add_user_content(user.id, content_create)


@router.patch("/me/content/{content_id}")
async def update_user_content(content_id: int, content_update: UserContentUpdate, user: ICurrentUser, content_service: IContentService):
    content = await content_service.get_user_content(content_id)
    if content.user_id != user.id:
        raise exceptions.not_your_content
    await content_service.update_user_content(content_id, content_update)


@router.delete("/me/content/{content_id}")
async def delete_user_content(content_id: int, user: ICurrentUser, content_service: IContentService):
    content = await content_service.get_user_content(content_id)
    if content.user_id != user.id:
        raise exceptions.not_your_content
    await content_service.delete_user_content(content_id)

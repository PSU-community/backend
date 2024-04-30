from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from ...api.dependencies import (
    get_current_user,
    get_email_service,
    get_user_service,
    IAdminUser,
    validate_user_create,
)
from ...models.schemas.users import BaseUser, UserCreate, UserSchema
from ...services.email_sender_service import EmailSenderService
from ...services.user_service import UserService

__all__ = ("router",)

router = APIRouter(tags=["Users"], dependencies=[Depends(HTTPBearer(auto_error=False))])


@router.get("/users")
async def get_users(user_service: UserService = Depends(get_user_service)):
    return await user_service.get_users()


@router.post("/users")
async def create_user(
    admin_user: IAdminUser,
    user_create: UserCreate = Depends(validate_user_create),
    user_service: UserService = Depends(get_user_service),
    email_service: EmailSenderService = Depends(get_email_service),
):
    user = await user_service.add_user(user_create)
    email_service.send_verification_email(user)


@router.get("/users/me")
async def get_me(user: UserSchema = Depends(get_current_user())) -> BaseUser:
    return user.to_base_user()


@router.get("/users/{user_id}")
async def get_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    return await user_service.get_user(user_id=user_id)
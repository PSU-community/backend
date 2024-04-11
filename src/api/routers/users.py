from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from ..auth import TokenTypes
from ...api import auth
from ...api.dependencies import get_current_user, get_user_service, validate_auth_user, validate_user_create
from ...models.schemas.auth import Token
from ...models.schemas.users import BaseUser, UserCreate, UserSchema
from ...services.user_service import UserService

__all__ = ("router", )

router = APIRouter(
    tags=["Users"],
    dependencies=[Depends(HTTPBearer(auto_error=False))]
)


@router.post("/users")
async def create_user(
    user_create: UserCreate = Depends(validate_user_create),
    user_service: UserService = Depends(get_user_service)
):
    await user_service.add_user(user_create)

    return {"status": "success"}


@router.get("/users/me")
async def get_me(user: UserSchema = Depends(get_current_user())) -> BaseUser:
    return user.to_base_user()


@router.post("/login")
async def login_user(user: UserSchema = Depends(validate_auth_user)) -> Token:
    return Token(
        access_token=auth.create_access_token(user.id),
        refresh_token=auth.create_refresh_token(user.id)
    )


@router.post("/refresh", response_model_exclude_none=True)
async def auth_refresh_jwt(user: UserSchema = Depends(get_current_user(TokenTypes.REFRESH))) -> Token:
    return Token(access_token=auth.create_access_token(user.id))

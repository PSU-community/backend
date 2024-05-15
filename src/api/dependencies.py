from typing import Annotated

from fastapi import Cookie, Depends, Form, HTTPException, status, UploadFile
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

from .auth import TokenData, TokenTypes
from ..api import auth, exceptions
from ..models.enums import UserPermissions
from ..models.schemas.create import CreateMediaSchema
from ..models.schemas.users import UserCreate, UserSchema
from ..repositories.rusender_repository import RuSenderRepository
from ..services.content_service import ContentService
from ..services.email_sender_service import EmailSenderService
from ..services.user_service import UserService
from ..repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/signin", auto_error=False)


def get_user_service():
    return UserService(UserRepository)


def get_content_service():
    return ContentService()


def get_email_service():
    return EmailSenderService(RuSenderRepository())


def get_current_token_data(
    token: str = Depends(oauth2_scheme),
    access_token: str = Cookie(default=None),
    refresh_token: str = Cookie(default=None),
):
    print(f"{token=}, {access_token=}, {refresh_token=}")
    _token = token or access_token or refresh_token

    if not _token:
        raise exceptions.missing_token

    try:
        return auth.decode_access_token(_token)
    except ExpiredSignatureError:
        raise exceptions.expired_token
    except InvalidTokenError:
        raise exceptions.invalid_token_type


def get_current_user(token_type: TokenTypes = TokenTypes.ACCESS):
    async def wrapper(
        service: UserService = Depends(get_user_service),
        token: TokenData = Depends(get_current_token_data),
    ):
        if token["type"] != token_type:
            raise exceptions.invalid_token
        return await service.get_user(user_id=int(token["sub"]))

    return wrapper


def get_current_user_from_email_token(token: str, service: UserService):
    data = get_current_token_data(token)
    return get_current_user(TokenTypes.EMAIL_VERIFICATION)(service, data)


async def validate_auth_user(
    email: str = Form(),
    password: str = Form(),
    service: UserService = Depends(get_user_service),
):
    user = await service.get_user(email=email)

    if not user:
        raise exceptions.invalid_credentials
    if not auth.verify_password_hash(password, user.hashed_password):
        raise exceptions.invalid_credentials

    return user


async def validate_user_register(
    name: str = Form(),
    email: str = Form(),
    password: str = Form(),
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.get_user(email=email)
    if user is not None:
        raise exceptions.invalid_credentials

    return UserCreate(name=name, email=email, password=password)


async def validate_user_create(
    name: str = Form(),
    email: str = Form(),
    password: str = Form(),
    permissions: UserPermissions = Form(),
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.get_user(email=email)
    if user is not None:
        raise exceptions.invalid_credentials

    return UserCreate(
        name=name, email=email, password=password, permissions=permissions
    )


IUserService = Annotated[UserService, Depends(get_user_service)]
IContentService = Annotated[ContentService, Depends(get_content_service)]
ICurrentUser = Annotated[UserSchema, Depends(get_current_user(TokenTypes.ACCESS))]


async def get_admin_user(user: ICurrentUser):
    if not user.is_admin:
        raise exceptions.missing_permissions

    return user


IAdminUser = Annotated[UserSchema, Depends(get_admin_user)]

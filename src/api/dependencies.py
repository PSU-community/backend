from fastapi import Depends, Form, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from .auth import TokenData, TokenTypes
from ..api import auth, exceptions
from ..models.schemas.users import UserCreate
from ..services.user_service import UserService
from ..repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_user_service():
    return UserService(UserRepository)


def get_current_token_data(token: str = Depends(oauth2_scheme)):
    try:
        return auth.decode_access_token(token)
    except InvalidTokenError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Invalid bearer token"
        )


def get_current_user(token_type: TokenTypes = TokenTypes.ACCESS):
    async def wrapper(
        service: UserService = Depends(get_user_service),
        token: TokenData = Depends(get_current_token_data)
    ):
        if token["type"] != token_type:
            raise exceptions.invalid_token_type
        return await service.get_user(user_id=int(token["sub"]))
    return wrapper


async def validate_auth_user(
    email: str = Form(),
    password: str = Form(),
    service: UserService = Depends(get_user_service)
):
    user = await service.get_user(email=email)

    if not user:
        raise exceptions.invalid_credentials
    if not auth.verify_password_hash(password, user.hashed_password):
        raise exceptions.invalid_credentials

    return user


async def validate_user_create(
    name: str = Form(),
    email: str = Form(),
    password: str = Form(),
    user_service: UserService = Depends(get_user_service)
):
    user = await user_service.get_user(email=email)
    if user is not None:
        raise exceptions.invalid_credentials

    return UserCreate(name=name, email=email, password=password)

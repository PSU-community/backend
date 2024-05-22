from pydantic import BaseModel, Field

from src.models.enums import UserPermissions


class BaseUser(BaseModel):
    name: str
    email: str
    is_verified: bool = Field(default=False)
    permissions: UserPermissions = Field(default=UserPermissions(0))


class UserSchema(BaseUser):
    id: int
    hashed_password: bytes

    def to_base_user(self):
        return BaseUser(name=self.name, email=self.email, is_verified=self.is_verified, permissions=self.permissions)

    @property
    def is_admin(self):
        return UserPermissions.ADMINISTRATOR in self.permissions


class UserCreate(BaseUser):
    password: str

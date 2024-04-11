from pydantic import BaseModel


class BaseUser(BaseModel):
    name: str
    email: str


class UserSchema(BaseUser):
    id: int
    hashed_password: bytes
    permissions: int

    def to_base_user(self):
        return BaseUser(
            name=self.name,
            email=self.email
        )


class UserCreate(BaseUser):
    password: str


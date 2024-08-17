from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDB(UserSchema):
    id: UUID


class UserPublic(BaseModel):
    id: UUID
    username: str
    email: EmailStr


class UserList(BaseModel):
    users: list[UserPublic]

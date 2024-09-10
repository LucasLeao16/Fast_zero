from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDB(UserSchema):
    id: int


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime | None = None
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]

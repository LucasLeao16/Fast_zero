from datetime import datetime
from enum import Enum

from pydantic import BaseModel

# from datetime import datetime


class TodoState(str, Enum):
    draft = "draft"
    todo = "todo"
    doing = "doing"
    done = "done"
    trash = "trash"


class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState


class TodoPublic(TodoSchema):
    id: int
    created_at: datetime
    updated_at: datetime | None = None


class TodoList(BaseModel):
    todos: list[TodoPublic]


class TodoUpdate(BaseModel):
    title: str | None = None
    descripition: str | None = None
    state: TodoState | None = None

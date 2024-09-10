from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

from fast_zero.schemas.todo import TodoState

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now(), nullable=True
    )
    todos: Mapped[list["Todo"]] = relationship(
        init=False, back_populates="user", cascade="all, delete-orphan"
    )


@table_registry.mapped_as_dataclass
class Todo:
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    state: Mapped[TodoState]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now(), nullable=True
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped[User] = relationship(init=False, back_populates="todos")

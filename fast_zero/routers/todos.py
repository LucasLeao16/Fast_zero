from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select

from fast_zero.models import Todo
from fast_zero.schemas.todo import TodoList, TodoPublic, TodoSchema, TodoUpdate
from fast_zero.types.index import T_CurrentUser, T_Session

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("/", response_model=TodoPublic)
def create_todo(
    todo: TodoSchema,
    user: T_CurrentUser,
    session: T_Session,
):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.get("/", response_model=TodoList)
def list_todos(  # noqa
    session: T_Session,
    user: T_CurrentUser,
    title: str = Query(None),
    description: str = Query(None),
    state: str = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    query = select(Todo).where(Todo.user_id == user.id)

    if title:
        query = query.filter(Todo.title.contains(title))

    if description:
        query = query.filter(Todo.description.contains(description))

    if state:
        query = query.filter(Todo.state == state)

    todos = session.scalars(query.offset(offset).limit(limit)).all()

    return {"todos": todos}


@router.delete("/{todo_id}")
def delete_todo(todo_id: int, session: T_Session, user: T_CurrentUser):
    todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Task not found."
        )

    session.delete(todo)
    session.commit()

    return {"message": "Task has been deleted successfully."}


@router.patch("/{todo_id}", response_model=TodoPublic)
def patch_todo(
    todo_id: int, session: T_Session, user: T_CurrentUser, todo: TodoUpdate
):
    db_todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not db_todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Task not found."
        )

    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo

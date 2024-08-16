from http import HTTPStatus
from uuid import uuid4

from fastapi import FastAPI

from fast_zero.entities.user import UserDB, UserList, UserPublic, UserSchema

app = FastAPI()

database = []


@app.get("/", status_code=HTTPStatus.OK)
def read_root():
    return {"message": "Olá mundo"}


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def creat_user(user: UserSchema):
    user_with_id = UserDB(id=uuid4(), **user.model_dump())
    database.append(user_with_id)
    return user_with_id


@app.get("/users/", status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
    return {"users": database}


@app.put("/users/{user_id}")
def update_user(user_id: str, user: UserSchema):
    pass


@app.delete("/users/{user_id}")
def delete_user(user_id: str, user: UserSchema):
    pass

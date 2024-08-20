from http import HTTPStatus

from fast_zero.schemas.user import UserPublic


def test_create_user(client):
    response = client.post(
        "/users",
        json={
            "username": "Noctis",
            "email": "lucii@gmail.com",
            "password": "Versus13",
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "Noctis",
        "email": "lucii@gmail.com",
        "id": 1,
    }


def test_username_allready_exist(client, user):
    response = client.post(
        "/users",
        json={
            "username": "Teste",
            "email": "teste@test.com",
            "password": "testtest",
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_email_allready_exist(client, user):
    response = client.post(
        "/users",
        json={
            "username": "Megumi",
            "email": "teste@test.com",
            "password": "testtest",
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get("/users/")
    assert response.json() == {"users": [user_schema]}

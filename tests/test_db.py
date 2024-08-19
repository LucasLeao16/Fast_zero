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


def test_update_user(client, user):
    response = client.put(
        "/users/1",
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "bob",
        "email": "bob@example.com",
        "id": 1,
    }


def test_update_user_not_exist(client, user):
    response = client.put(
        "/users/0",
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client, user):
    response = client.delete("/users/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}


def test_delete_user_not_exist(client, user):
    response = client.delete("/users/0")
    assert response.status_code == HTTPStatus.NOT_FOUND

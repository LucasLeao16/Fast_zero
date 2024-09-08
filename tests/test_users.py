from http import HTTPStatus


def test_read_users(client):
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "testusername",
            "password": "testpassword",
            "email": "test@test.com",
        },
    )

    assert response.status_code == HTTPStatus.CREATED


def test_update_user(client, user, token):
    response = client.put(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
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
        "id": user.id,
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

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_delete_user(client, user, token):
    response = client.delete(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}


def test_delete_user_not_exist(client, user):
    response = client.delete("/users/0")
    assert response.status_code == HTTPStatus.UNAUTHORIZED

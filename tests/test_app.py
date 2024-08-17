from http import HTTPStatus


def test__read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Olá mundo"}


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


def test_read_users(client):
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK


def test_update_user(client):
    pass


def test_delete_user(client):
    pass

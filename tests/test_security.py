from http import HTTPStatus

import pytest
from fastapi.exceptions import HTTPException
from jwt import decode

from fast_zero.utils.security import (
    create_access_token,
    get_current_user,
    settings,
)


def test_jwt():
    data = {"sub": "test@test.com"}
    token = create_access_token(data)

    decoded = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert decoded["sub"] == data["sub"]
    assert decoded["exp"]  # Testa se o valor de exp foi adicionado ao token


def test_jwt_invalid_token(client):
    response = client.delete(
        "/users/1", headers={"Authorization": "Bearer token-invalido"}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


def test_get_current_user_cant_decod_token():
    with pytest.raises(HTTPException):
        get_current_user([])


def test_get_current_user_without_username(session):
    token = create_access_token(data={"bub": "test@gmail.com"})
    with pytest.raises(HTTPException):
        get_current_user(session, token)


def test_get_current_user_username_not_found(session):
    token = create_access_token(data={"sub": "cloud@gmail.com"})
    with pytest.raises(HTTPException):
        get_current_user(session, token)

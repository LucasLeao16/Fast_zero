from uuid import uuid4

from sqlalchemy import select

from fast_zero.models.User import User


def test_create_user(session):
    user = User(
        id=uuid4(),
        username="Noctis",
        email="lucii@gmail.com",
        password="Versus13",
    )

    session.add(user)
    session.commit()
    result = session.scalar(
        select(User).where(User.email == "lucii@gmail.com")
    )

    assert result.username == "Noctis"

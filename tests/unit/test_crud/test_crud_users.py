from typing import List

from app.crud.users import create_user, get_users
from app.models.users import User


def test_create_user(db_session):
    user_data = {"name": "Test User", "email": "test@example.com"}
    created_user: User = create_user(db_session, user_data)

    assert created_user.id is not None
    assert created_user.name == user_data["name"]
    assert created_user.email == user_data["email"]


def test_get_users(db_session):
    user1 = User(name="User 1", email="user1@example.com")
    user2 = User(name="User 2", email="user2@example.com")

    db_session.add_all([user1, user2])
    db_session.commit()

    users: List[User] = get_users(db_session)

    assert len(users) == 2
    assert users[0].email == "user1@example.com"
    assert users[1].email == "user2@example.com"

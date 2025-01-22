import pytest
from sqlalchemy.exc import IntegrityError

from app.models.users import User


def test_database_connection(db_session):
    result = db_session.execute("SELECT 1")
    assert result.scalar() == 1


def test_user_table_creation(db_session):
    new_user = User(name="Test User", email="test@example.com")
    db_session.add(new_user)
    db_session.commit()

    user = db_session.query(User).filter(User.email == "test@example.com").first()
    assert user is not None
    assert user.name == "Test User"


def test_unique_email_constraint(db_session):
    user1 = User(name="User 1", email="test@example.com")
    db_session.add(user1)
    db_session.commit()

    user2 = User(name="User 2", email="test@example.com")
    db_session.add(user2)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()


def test_transaction_rollback(db_session):
    user1 = User(name="Valid User", email="valid@example.com")
    db_session.add(user1)

    user2 = User(email="invalid@example.com")  # Missing name
    db_session.add(user2)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()
    assert db_session.query(User).count() == 0


def test_null_constraints(db_session):
    with pytest.raises(IntegrityError):
        user = User(email="nulltest@example.com")  # Missing name
        db_session.add(user)
        db_session.commit()

    db_session.rollback()


def test_indexes(db_session):
    import time

    for i in range(100):
        user = User(name=f"User {i}", email=f"user{i}@example.com")
        db_session.add(user)
    db_session.commit()

    start = time.time()
    db_session.query(User).filter(User.email == "user99@example.com").first()
    indexed_time = time.time() - start

    start = time.time()
    db_session.query(User).filter(User.name == "User 99").first()
    non_indexed_time = time.time() - start

    assert indexed_time < non_indexed_time


def test_database_teardown(db_session):
    user = User(name="Teardown User", email="teardown@example.com")
    db_session.add(user)
    db_session.commit()

    assert db_session.query(User).count() == 1

    db_session.query(User).delete()
    db_session.commit()

    assert db_session.query(User).count() == 0

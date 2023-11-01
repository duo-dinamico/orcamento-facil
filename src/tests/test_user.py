import pytest

from .conftest import db_session, valid_user
from ..modules.db_crud import create_user, read_user_by_name
from ..modules.db_models import User


# DEFAULT BEHAVIOUR


def test_success_user_creation(db_session):
    user = create_user(db_session, "username", "password")

    assert type(user) is int
    assert user == 1


def test_success_read_user_by_name(db_session, valid_user):
    user = read_user_by_name(db_session, "validUser")
    print(f"test: {user} {type(user)}")

    assert user.id == 1
    assert user.username == "validUser"


# ERROR HANDLING


def test_error_username_exist(db_session, valid_user):
    user = create_user(db_session, "validUser", "password")

    assert user is None


def test_error_read_user_by_name(db_session, valid_user):
    user = read_user_by_name(db_session, "wrongUser")
    print(f"test: {user} {type(user)}")

    assert user is None

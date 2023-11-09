import pytest

from ..modules.db.db_crud_user import create_user, login_user, read_user_by_id, read_user_by_name
from .conftest import db_session, valid_user

#
# DEFAULT BEHAVIOUR
#


def test_success_user_creation(db_session):
    user_id = create_user(db_session, "username", "password")

    assert type(user_id) is int
    assert user_id == 1


def test_success_read_user_by_name(db_session, valid_user):
    user = read_user_by_name(db_session, "validUser")

    assert user.id == 1
    assert user.username == "validUser"


def test_success_read_user_by_id(db_session, valid_user):
    user = read_user_by_id(db_session, 1)

    assert user.id == 1
    assert user.username == "validUser"


def test_success_user_login(db_session, valid_user):
    user_id = login_user(db_session, "validUser", "ValidPassword1")

    assert type(user_id) is int
    assert user_id == 1


#
# ERROR HANDLING
#


def test_error_username_exist(db_session, valid_user):
    user = create_user(db_session, "validUser", "password")

    assert user is None


def test_error_read_user_by_name(db_session, valid_user):
    user = read_user_by_name(db_session, "wrongUser")

    assert user is None


def test_error_read_user_by_id(db_session, valid_user):
    user = read_user_by_id(db_session, 127)

    assert user is None


def test_error_login_no_user(db_session, valid_user):
    user = login_user(db_session, "username", "ValidPassword1")

    assert user is None


def test_error_login_wrong_password(db_session, valid_user):
    user = login_user(db_session, "validUser", "password")

    assert user is None

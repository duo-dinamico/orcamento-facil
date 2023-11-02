import pytest

from .conftest import db_session, valid_user, valid_account
from ..modules.db_crud import (
    create_user,
    read_user_by_name,
    read_user_by_id,
    login_user,
    read_account_by_name,
    read_account_by_id,
    create_account,
)


# DEFAULT BEHAVIOUR


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


def test_success_account_read_by_id(db_session, valid_account):
    account = read_account_by_id(db_session, 1)

    assert account.id == 1
    assert account.name == "validAccount"


def test_success_account_creation(db_session, valid_user):
    account_id = create_account(db_session, user_id=1, account_name="accountName")

    assert type(account_id) is int
    assert account_id == 1


# ERROR HANDLING


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


def test_error_account_read_by_id(db_session, valid_account):
    user = read_account_by_id(db_session, 5)

    assert user is None


def test_error_account_creation_invalid_user(db_session, valid_account):
    account_id = create_account(db_session, user_id=2, account_name="accountName")

    assert account_id is None


def test_error_account_creation_invalid_name(db_session, valid_account):
    account_id = create_account(db_session, user_id=1, account_name="validAccount")

    assert account_id is None

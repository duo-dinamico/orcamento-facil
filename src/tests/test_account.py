import pytest

from .conftest import db_session, valid_user, valid_account
from ..modules.db_crud import (
    read_account_by_name,
    read_account_by_id,
    create_account,
    read_user_accounts,
    delete_account,
)


#
# DEFAULT BEHAVIOUR
#


def test_success_account_read_by_id(db_session, valid_account):
    account = read_account_by_id(db_session, 1)

    assert account.id is 1
    assert account.name == "validAccount"


def test_success_account_read_by_name(db_session, valid_account):
    account_id = read_account_by_name(db_session, account_name="validAccount")

    assert account_id is 1


def test_success_account_creation(db_session, valid_user):
    account_id = create_account(db_session, user_id=1, account_name="accountName")

    assert type(account_id) is int
    assert account_id is 1


def test_success_account_read_user_accounts(db_session, valid_account):
    account_list = read_user_accounts(db_session, user_id=1)

    assert type(account_list) is list
    assert len(account_list) > 0


def test_success_account_deletion(db_session, valid_account):
    result = delete_account(db_session, account_id=1, user_id=1)

    assert result is True


#
# ERROR HANDLING
#


def test_error_account_read_by_id(db_session, valid_account):
    user = read_account_by_id(db_session, 5)

    assert user is None


def test_error_account_read_by_name(db_session, valid_account):
    account_id = read_account_by_name(db_session, account_name="wrongAccount")

    assert account_id is None


def test_error_account_creation_invalid_user(db_session, valid_account):
    account_id = create_account(db_session, user_id=2, account_name="accountName")

    assert account_id is None


def test_error_account_creation_invalid_name(db_session, valid_account):
    account_id = create_account(db_session, user_id=1, account_name="validAccount")

    assert account_id is None


def test_error_account_creation_invalid_type(db_session, valid_user):
    account_id = create_account(
        db_session, user_id=1, account_name="validAccount", account_type="STUPID"
    )

    assert account_id is None


def test_error_account_read_user_accounts_invalid_user(db_session):
    account_list = read_user_accounts(db_session, user_id=1)

    assert account_list is None


def test_error_acccount_delete_wrong_account_id(db_session, valid_account):
    result = delete_account(db_session, account_id=2, user_id=1)

    assert result is False


def test_error_acccount_delete_wrong_user_id(db_session, valid_account):
    result = delete_account(db_session, account_id=1, user_id=2)

    assert result is False

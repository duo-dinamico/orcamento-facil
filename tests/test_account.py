import pytest

from ..modules.db.db_crud_account import (
    create_account,
    delete_account,
    read_account_by_id,
    read_account_by_name,
    read_account_incomes,
)
from ..modules.db.db_crud_user import read_user_accounts
from .conftest import db_session, valid_account, valid_user

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


def test_success_account_deletion(db_session, valid_account):
    result = delete_account(db_session, account_id=1, user_id=1)

    assert result is True


def test_success_account_incomes_list(db_session, valid_income):
    income_list = read_account_incomes(db_session, account_id=1)

    assert type(income_list) is list
    assert len(income_list) > 0


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
    account_id = create_account(db_session, user_id=1, account_name="validAccount", account_type="STUPID")

    assert account_id is None


def test_error_acccount_delete_wrong_account_id(db_session, valid_account):
    result = delete_account(db_session, account_id=2, user_id=1)

    assert result is False


def test_error_acccount_delete_wrong_user_id(db_session, valid_account):
    result = delete_account(db_session, account_id=1, user_id=2)

    assert result is False


def test_error_account_income_list_invalid_account(db_session):
    income_list = read_account_incomes(db_session, account_id=1)

    assert income_list is None

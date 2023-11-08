import pytest

from ..modules.db.dc_crud_income import create_income, read_income_by_name
from .conftest import valid_account

#
# DEFAULT BEHAVIOUR
#


def test_success_income_read_by_name(db_session, valid_income):
    income_id = read_income_by_name(db_session, account_id=1, name="validIncome")

    assert income_id is 1


def test_success_income_creation(db_session, valid_account):
    income_id = create_income(db_session, account_id=1, name="newIncome")

    assert type(income_id) is int
    assert income_id == 1


#
# ERROR HANDLING
#


def test_error_income_read_by_name(db_session, valid_income):
    income_id = read_income_by_name(db_session, account_id=1, name="wrongAccount")
    print("Teste")

    assert income_id is None


def test_error_income_creation_invalid_account(db_session):
    income_id = create_income(db_session, account_id=1, name="newIncome")

    assert income_id is None


def test_error_income_creation_invalid_name(db_session, valid_income):
    income_id = create_income(db_session, account_id=1, name="validIncome")

    assert income_id is None

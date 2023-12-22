from datetime import datetime

import pytest

from ezbudget.model import Model
from ezbudget.utils import get_hashed_password


@pytest.fixture(name="db_session")
def fixture_db_session():
    model = Model("test")
    try:
        yield model
    finally:
        model.close_session()


@pytest.fixture(name="valid_user")
def fixture_valid_user(db_session):
    db_session.model_user.create_user(username="validUser", password=get_hashed_password("ValidPassword1"))


@pytest.fixture(name="valid_account")
def fixture_valid_account(db_session, valid_user):
    _ = valid_user
    db_session.model_account.create_account(user_id=1, name="validAccount")


@pytest.fixture(name="valid_category")
def fixture_valid_category(db_session):
    db_session.model_category.create_category(name="validCategory")


@pytest.fixture()
def second_valid_category(db_session):
    db_session.model_category.create_category(name="secondvalidCategory")


@pytest.fixture(name="valid_subcategory")
def fixture_valid_subcategory(db_session, valid_category):
    _ = valid_category
    db_session.model_subcategory.create_subcategory(category_id=1, name="validSubCategory")


@pytest.fixture()
def valid_income(db_session, valid_account, valid_user):
    _ = valid_account
    _ = valid_user
    db_session.model_income.create_income(account_id=1, user_id=1, name="validIncome")


@pytest.fixture()
def valid_income_second(db_session, valid_account, valid_user):
    _ = valid_account
    _ = valid_user
    db_session.model_income.create_income(account_id=1, user_id=1, name="validIncomeSecond")


@pytest.fixture()
def valid_transaction(db_session, valid_account, valid_subcategory):
    _ = valid_account
    _ = valid_subcategory
    db_session.model_transaction.create_transaction(
        account_id=1, subcategory_id=1, date=datetime(2022, 12, 12), value=100, description="validTransaction"
    )


@pytest.fixture()
def valid_user_subcategory(db_session, valid_user, valid_subcategory):
    _ = valid_user
    _ = valid_subcategory
    db_session.model_user_subcategory.create_user_subcategory(user_id=1, subcategory_id=1)

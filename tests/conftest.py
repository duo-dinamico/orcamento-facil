from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ezbudget.model import Account, Base, Category, Income, SubCategory, Transaction, User
from ezbudget.utils import get_hashed_password

engine = create_engine("sqlite:///test.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(name="db_session")
def fixture_db_session():
    Base.metadata.create_all(engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)
        # session.rollback()
        # session.close()


@pytest.fixture(name="valid_user")
def fixture_valid_user(db_session):
    db_session.add(User(username="validUser", password=get_hashed_password("ValidPassword1")))
    db_session.commit()


@pytest.fixture(name="valid_account")
def fixture_valid_account(db_session, valid_user):
    _ = valid_user
    db_session.add(Account(user_id=1, name="validAccount"))
    db_session.commit()


@pytest.fixture(name="valid_category")
def fixture_valid_category(db_session):
    db_session.add(Category(name="validCategory"))
    db_session.commit()


@pytest.fixture()
def second_valid_category(db_session):
    db_session.add(Category(name="secondvalidCategory"))
    db_session.commit()


@pytest.fixture(name="valid_subcategory")
def fixture_valid_subcategory(db_session, valid_category):
    _ = valid_category
    db_session.add(SubCategory(category_id=1, name="validSubCategory"))
    db_session.commit()


@pytest.fixture()
def valid_income(db_session, valid_account):
    _ = valid_account
    db_session.add(Income(account_id=1, name="validIncome"))
    db_session.commit()


@pytest.fixture()
def valid_income_second(db_session, valid_account):
    _ = valid_account
    db_session.add(Income(account_id=1, name="validIncomeSecond"))
    db_session.commit()


@pytest.fixture()
def valid_transaction(db_session, valid_account, valid_subcategory):
    _ = valid_account
    _ = valid_subcategory
    db_session.add(
        Transaction(
            account_id=1,
            subcategory_id=1,
            date=datetime(2022, 12, 12),
            value=100,
            description="validTransaction",
        )
    )
    db_session.commit()

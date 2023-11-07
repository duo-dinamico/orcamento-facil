import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..modules.db.db_models import Account, Base, Category, SubCategory, User
from ..modules.utils.hash import get_hashed_password

engine = create_engine("sqlite:///test.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def db_session():
    Base.metadata.create_all(engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)
        # session.rollback()
        # session.close()


@pytest.fixture()
def valid_user(db_session):
    db_session.add(User(username="validUser", password=get_hashed_password("ValidPassword1")))
    db_session.commit()


@pytest.fixture()
def valid_account(db_session, valid_user):
    db_session.add(Account(user_id=1, name="validAccount"))
    db_session.commit()


@pytest.fixture()
def valid_category(db_session):
    db_session.add(Category(name="validCategory"))
    db_session.commit()


@pytest.fixture()
def second_valid_category(db_session):
    db_session.add(Category(name="secondvalidCategory"))
    db_session.commit()


@pytest.fixture()
def valid_subcategory(db_session, valid_category):
    db_session.add(SubCategory(category_id=1, name="validSubCategory"))
    db_session.commit()

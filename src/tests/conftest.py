import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..modules.db_models import Base


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

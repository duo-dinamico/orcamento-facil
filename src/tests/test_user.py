import pytest

from .conftest import db_session
from ..modules.db_crud import create_user
from ..modules.db_models import User


# DEFAULT BEHAVIOUR
# @pytest
def test_success_user_creation(db_session):
    user = create_user(db_session, "username", "password")
    print(f"test: {user}")

    assert type(user) is int
    assert user == 1

import pytest

from .conftest import db_session, valid_category
from ..modules.db.db_crud_category import create_category, read_category_by_name

#
# DEFAULT BEHAVIOUR
#


def test_success_read_category_by_name(db_session, valid_category):
    category_id = read_category_by_name(db_session, "validCategory")

    assert type(category_id) is int
    assert category_id == 1


def test_success_category_creation(db_session):
    category_id = create_category(db_session, name="newCategory")

    assert type(category_id) is int
    assert category_id == 1


#
# ERROR HANDLING
#


def test_error_read_category_by_name(db_session, valid_category):
    category_id = read_category_by_name(db_session, "wrongCategory")

    assert category_id == None


def test_success_category_creation_name_exist(db_session, valid_category):
    category_id = create_category(db_session, name="validCategory")

    assert category_id == None

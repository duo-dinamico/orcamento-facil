import pytest

from ..modules.db.db_crud_subcategory import (
    create_subcategory,
    read_subcategory_by_name,
    read_subcategory_list_by_category_id,
)
from .conftest import db_session, valid_category

#
# DEFAULT BEHAVIOUR
#


def test_success_read_subcategory_by_name(db_session, valid_subcategory):
    subcategory_id = read_subcategory_by_name(db_session, "validSubCategory")

    assert type(subcategory_id) is int
    assert subcategory_id == 1


def test_success_read_category_list_by_category_id(db_session, valid_subcategory):
    category_list = read_subcategory_list_by_category_id(db_session, category_id=1)

    assert type(category_list) is list
    assert len(category_list) == 1


def test_success_subcategory_creation(db_session, valid_category):
    subcategory_id = create_subcategory(db_session, category_id=1, name="newSubCategory")

    assert type(subcategory_id) is int
    assert subcategory_id == 1


#
# ERROR HANDLING
#


def test_error_read_subcategory_by_name(db_session, valid_subcategory):
    subcategory_id = read_subcategory_by_name(db_session, "wrongSubCategory")

    assert subcategory_id == None


def test_error_read_subcategory_list_dont_exist(db_session, valid_category):
    category_list = read_subcategory_list_by_category_id(db_session, category_id=1)

    assert category_list == None


def test_error_read_subcategory_list_by_category_id_category_invalid(db_session, valid_subcategory):
    category_list = read_subcategory_list_by_category_id(db_session, category_id=2)

    assert category_list == None


def test_error_subcategory_creation_category_invalid(db_session):
    subcategory_id = create_subcategory(db_session, category_id=1, name="validSubCategory")

    assert subcategory_id == None


def test_error_subcategory_creation_name_exist(db_session, valid_subcategory):
    subcategory_id = create_subcategory(db_session, category_id=1, name="validSubCategory")

    assert subcategory_id == None


def test_error_subcategory_creation_recurrent_not_bool(db_session, valid_category):
    subcategory_id = create_subcategory(
        db_session, category_id=1, name="validSubCategory", recurrent="x"
    )

    assert subcategory_id == None


def test_error_subcategory_creation_recurrency_invalid(db_session, valid_category):
    subcategory_id = create_subcategory(
        db_session, category_id=1, name="validSubCategory", recurrency="sometime"
    )

    assert subcategory_id == None

from ezbudget.modules.db.db_crud_category import create_category, read_category_by_id, read_category_by_name, read_category_list

#
# DEFAULT BEHAVIOUR
#


def test_success_read_category_by_name(db_session, valid_category):
    _ = valid_category
    category_id = read_category_by_name(db_session, "validCategory")

    assert isinstance(category_id, int)
    assert category_id == 1


def test_success_read_category_by_id(db_session, valid_category):
    _ = valid_category
    category = read_category_by_id(db_session, category_id=1)

    assert category.name == "validCategory"
    assert category.id == 1


def test_success_read_category_list(db_session, valid_category):
    _ = valid_category
    category_list = read_category_list(db_session)

    assert isinstance(category_list, list)
    assert len(category_list) == 1


def test_success_category_creation(db_session):
    category_id = create_category(db_session, name="newCategory")

    assert isinstance(category_id, int)
    assert category_id == 1


#
# ERROR HANDLING
#


def test_error_read_category_by_name(db_session, valid_category):
    _ = valid_category
    category_id = read_category_by_name(db_session, "wrongCategory")

    assert category_id is None


def test_error_read_category_by_id(db_session, valid_category):
    _ = valid_category
    category = read_category_by_id(db_session, category_id=2)

    assert category is None


def test_error_read_category_list(db_session):
    category_list = read_category_list(db_session)

    assert category_list is None


def test_error_category_creation_name_exist(db_session, valid_category):
    _ = valid_category
    category_id = create_category(db_session, name="validCategory")

    assert category_id is None

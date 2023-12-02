#
# DEFAULT BEHAVIOUR
#


def test_success_read_subcategory_by_name(db_session, valid_subcategory):
    _ = valid_subcategory
    subcategory = db_session.read_subcategory_by_name("validSubCategory")

    assert isinstance(subcategory.id, int)
    assert subcategory.id == 1


def test_success_read_category_list_by_category_id(db_session, valid_subcategory):
    _ = valid_subcategory
    category_list = db_session.read_subcategories_by_category_id(category_id=1)

    assert isinstance(category_list, list)
    assert len(category_list) == 1


def test_success_read_subcategories(db_session, valid_subcategory):
    _ = valid_subcategory
    subcategory_list = db_session.read_subcategories()

    assert isinstance(subcategory_list, list)
    assert len(subcategory_list) == 1


def test_success_subcategory_creation(db_session, valid_category):
    _ = valid_category
    subcategory = db_session.create_subcategory(category_id=1, name="newSubCategory")

    assert isinstance(subcategory.id, int)
    assert subcategory.id == 1


#
# ERROR HANDLING
#


def test_error_read_subcategory_by_name(db_session, valid_subcategory):
    _ = valid_subcategory
    subcategory_id = db_session.read_subcategory_by_name("wrongSubCategory")

    assert subcategory_id is None


def test_error_read_subcategory_list_dont_exist(db_session, valid_category):
    _ = valid_category
    category_list = db_session.read_subcategories_by_category_id(category_id=1)

    assert len(category_list) < 1


def test_error_read_subcategory_list_by_category_id_category_invalid(db_session, valid_subcategory):
    _ = valid_subcategory
    category_list = db_session.read_subcategories_by_category_id(category_id=2)

    assert len(category_list) < 1


def test_error_read_subcategory_list_wrong_category(db_session, valid_subcategory, second_valid_category):
    _ = valid_subcategory
    _ = second_valid_category
    category_list = db_session.read_subcategories_by_category_id(category_id=2)

    assert len(category_list) < 1


def test_error_subcategory_creation_category_invalid(db_session):
    subcategory = db_session.create_subcategory(category_id=1, name="validSubCategory")

    assert subcategory == "Category ID does not exist"

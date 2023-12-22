#
# DEFAULT BEHAVIOUR
#


def test_success_read_category_by_name(db_session, valid_category):
    _ = valid_category
    category = db_session.model_category.read_category_by_name("validCategory")

    assert isinstance(category.id, int)
    assert category.id == 1


def test_success_read_category_by_id(db_session, valid_category):
    _ = valid_category
    category = db_session.model_category.read_category_by_id(id=1)

    assert category.name == "validCategory"
    assert category.id == 1


def test_success_read_category_list(db_session, valid_category):
    _ = valid_category
    category_list = db_session.model_category.read_categories()

    assert isinstance(category_list, list)
    assert len(category_list) == 1


def test_success_category_creation(db_session):
    category = db_session.model_category.create_category(name="newCategory")

    assert isinstance(category.id, int)
    assert category.id == 1
    assert category.name == "newCategory"


#
# ERROR HANDLING
#


def test_error_read_category_by_name(db_session, valid_category):
    _ = valid_category
    category_id = db_session.model_category.read_category_by_name("wrongCategory")

    assert category_id is None


def test_error_read_category_by_id(db_session, valid_category):
    _ = valid_category
    category = db_session.model_category.read_category_by_id(id=2)

    assert category is None


def test_error_read_category_list(db_session):
    categories = db_session.model_category.read_categories()

    assert len(categories) < 1


def test_error_category_creation_name_exist(db_session, valid_category):
    _ = valid_category
    category_id = db_session.model_category.create_category(name="validCategory")

    assert category_id == "Category already exists"

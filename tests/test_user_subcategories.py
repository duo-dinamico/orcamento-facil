# DEFAULT BEHAVIOUR


def test_success_create_user_subcategory(db_session, valid_user, valid_subcategory):
    _ = valid_user
    _ = valid_subcategory
    user_subcategory = db_session.model_user_subcategory.create_user_subcategory(user_id=1, subcategory_id=1)

    assert user_subcategory.user_id == 1
    assert user_subcategory.subcategory_id == 1


def test_success_create_user_subcategory_with_subcategory(db_session, valid_user, valid_subcategory):
    _ = valid_user
    _ = valid_subcategory
    user_subcategory = db_session.model_user_subcategory.create_user_subcategory(user_id=1, subcategory_id=1)

    assert user_subcategory.subcategory.name == "validSubCategory"


def test_success_read_user_subcategory_multiple_args(db_session, valid_user_subcategory):
    _ = valid_user_subcategory
    user_subcategory = db_session.model_user_subcategory.read_user_subcategories_multiple_args(
        user_id=1, subcategory_id=1
    )

    assert user_subcategory.id == 1


def test_success_read_user_subcategory_single_arg(db_session, valid_user_subcategory):
    _ = valid_user_subcategory
    user_subcategory = db_session.model_user_subcategory.read_user_subcategories_single_arg(key="user_id", value=1)

    assert user_subcategory.id == 1
    assert user_subcategory.user_id == 1


def test_success_read_user_subcategory_from_user(db_session, valid_user_subcategory):
    _ = valid_user_subcategory
    user_subcategory = db_session.model_user_subcategory.read_user_subcategories_by_user(user_id=1)

    assert len(user_subcategory) == 1
    for user in user_subcategory:
        assert user.user_id == 1


def test_success_delete_user_subcategory(db_session, valid_user_subcategory):
    _ = valid_user_subcategory
    deleted_rows = db_session.model_user_subcategory.delete_user_subcategory(subcategory_id=1)

    assert deleted_rows == 1


# ERROR HANDLING


def test_error_user_does_not_exist(db_session, valid_subcategory):
    _ = valid_subcategory
    user_subcategory = db_session.model_user_subcategory.create_user_subcategory(user_id=2, subcategory_id=1)

    assert user_subcategory == "Either User ID or SubCategory ID does not exist"


def test_error_subcategory_does_not_exist(db_session, valid_user):
    _ = valid_user
    user_subcategory = db_session.model_user_subcategory.create_user_subcategory(user_id=1, subcategory_id=2)

    assert user_subcategory == "Either User ID or SubCategory ID does not exist"


def test_error_user_subcategory_constrain_error(db_session, valid_user_subcategory):
    _ = valid_user_subcategory
    user_subcategory = db_session.model_user_subcategory.create_user_subcategory(user_id=1, subcategory_id=1)

    assert user_subcategory == "User ID and SubCategory ID combination must be unique"


def test_error_read_user_subcategory_multiple_args(db_session):
    user_subcategory = db_session.model_user_subcategory.read_user_subcategories_multiple_args(
        user_id=1, subcategory_id=1
    )

    assert user_subcategory is None


def test_error_read_user_subcategory_multiple_args_wrong_arg(db_session):
    user_subcategory = db_session.model_user_subcategory.read_user_subcategories_multiple_args(fish=1)

    assert user_subcategory == "AttributeError: type object 'UserSubCategory' has no attribute 'fish'"


def test_error_read_user_subcategory_single_arg(db_session):
    user_subcategory = db_session.model_user_subcategory.read_user_subcategories_single_arg(key="user_id", value=1)

    assert user_subcategory is None


def test_error_read_user_subcategory_single_arg_wrong_arg(db_session):
    user_subcategory = db_session.model_user_subcategory.read_user_subcategories_single_arg(key="fish", value=1)

    assert user_subcategory == "AttributeError: type object 'UserSubCategory' has no attribute 'fish'"


def test_error_read_user_subcategory_from_user(db_session, valid_user_subcategory):
    _ = valid_user_subcategory
    user_subcategory = db_session.model_user_subcategory.read_user_subcategories_by_user(user_id=2)

    assert len(user_subcategory) == 0

#
# DEFAULT BEHAVIOUR
#


def test_success_user_creation(db_session):
    user = db_session.model_user.create_user("username", "password")

    assert isinstance(user.id, int)
    assert user.id == 1


def test_success_read_user_by_name(db_session, valid_user):
    _ = valid_user
    user = db_session.model_user.read_user_by_name("validUser")

    assert user.id == 1
    assert user.username == "validUser"


def test_success_read_user_by_id(db_session, valid_user):
    _ = valid_user
    user = db_session.model_user.read_user_by_id(id=1)

    assert user.id == 1
    assert user.username == "validUser"


#
# ERROR HANDLING
#


def test_error_username_exist(db_session, valid_user):
    _ = valid_user
    user = db_session.model_user.create_user("validUser", "password")

    assert user == "User already exists"


def test_error_read_user_by_name(db_session, valid_user):
    _ = valid_user
    user = db_session.model_user.read_user_by_name("wrongUser")

    assert user is None


def test_error_read_user_by_id(db_session, valid_user):
    _ = valid_user
    user = db_session.model_user.read_user_by_id(id=127)

    assert user is None

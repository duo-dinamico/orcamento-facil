#
# DEFAULT BEHAVIOUR
#


def test_success_user_creation(db_session):
    user = db_session.create_user("username", "password")

    assert isinstance(user.id, int)
    assert user.id == 1


def test_success_read_user_by_name(db_session, valid_user):
    _ = valid_user
    user = db_session.read_user_by_name("validUser")

    assert user.id == 1
    assert user.username == "validUser"


def test_success_read_user_by_id(db_session, valid_user):
    _ = valid_user
    user = db_session.read_user_by_id(id=1)

    assert user.id == 1
    assert user.username == "validUser"


def test_success_user_accounts_list(db_session, valid_account):
    _ = valid_account
    account_list = db_session.read_accounts_by_user(user_id=1, account_type="BANK")

    assert isinstance(account_list, list)
    assert len(account_list) > 0


def test_success_user_incomes_list(db_session, valid_income, valid_income_second):
    _ = valid_income
    _ = valid_income_second
    income_list = db_session.read_incomes_by_user(user_id=1)

    assert isinstance(income_list, list)
    assert len(income_list) == 2


#
# ERROR HANDLING
#


def test_error_username_exist(db_session, valid_user):
    _ = valid_user
    user = db_session.create_user("validUser", "password")

    assert user == "User already exists"


def test_error_read_user_by_name(db_session, valid_user):
    _ = valid_user
    user = db_session.read_user_by_name("wrongUser")

    assert user is None


def test_error_read_user_by_id(db_session, valid_user):
    _ = valid_user
    user = db_session.read_user_by_id(id=127)

    assert user is None


def test_error_accounts_list_invalid_user(db_session):
    account_list = db_session.read_accounts_by_user(user_id=1, account_type="BANK")

    assert account_list == list()


def test_error_incomes_list_invalid_user(db_session):
    income_list = db_session.read_incomes_by_user(user_id=1)

    assert income_list == list()

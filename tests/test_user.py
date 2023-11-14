from ezbudget.modules.db.db_crud_user import (
    create_user,
    login_user,
    read_user_accounts,
    read_user_by_id,
    read_user_by_name,
    read_user_incomes,
)

#
# DEFAULT BEHAVIOUR
#


def test_success_user_creation(db_session):
    user_id = create_user(db_session, "username", "password")

    assert isinstance(user_id, int)
    assert user_id == 1


def test_success_read_user_by_name(db_session, valid_user):
    _ = valid_user
    user = read_user_by_name(db_session, "validUser")

    assert user.id == 1
    assert user.username == "validUser"


def test_success_read_user_by_id(db_session, valid_user):
    _ = valid_user
    user = read_user_by_id(db_session, 1)

    assert user.id == 1
    assert user.username == "validUser"


def test_success_user_login(db_session, valid_user):
    _ = valid_user
    user_id = login_user(db_session, "validUser", "ValidPassword1")

    assert isinstance(user_id, int)
    assert user_id == 1


def test_success_user_accounts_list(db_session, valid_account):
    _ = valid_account
    account_list = read_user_accounts(db_session, user_id=1)

    assert isinstance(account_list, list)
    assert len(account_list) > 0


def test_success_user_incomes_list(db_session, valid_income, valid_income_second):
    _ = valid_income
    _ = valid_income_second
    income_list = read_user_incomes(db_session, user_id=1)

    assert isinstance(income_list, list)
    assert len(income_list) == 2


#
# ERROR HANDLING
#


def test_error_username_exist(db_session, valid_user):
    _ = valid_user
    user = create_user(db_session, "validUser", "password")

    assert user is None


def test_error_read_user_by_name(db_session, valid_user):
    _ = valid_user
    user = read_user_by_name(db_session, "wrongUser")

    assert user is None


def test_error_read_user_by_id(db_session, valid_user):
    _ = valid_user
    user = read_user_by_id(db_session, 127)

    assert user is None


def test_error_login_no_user(db_session, valid_user):
    _ = valid_user
    user = login_user(db_session, "username", "ValidPassword1")

    assert user is None


def test_error_login_wrong_password(db_session, valid_user):
    _ = valid_user
    user = login_user(db_session, "validUser", "password")

    assert user is None


def test_error_accounts_list_invalid_user(db_session):
    account_list = read_user_accounts(db_session, user_id=1)

    assert account_list is None


def test_error_incomes_list_invalid_user(db_session):
    income_list = read_user_incomes(db_session, user_id=1)

    assert income_list is None

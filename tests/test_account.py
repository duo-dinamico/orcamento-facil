#
# DEFAULT BEHAVIOUR
#


def test_success_account_read_by_id(db_session, valid_account):
    _ = valid_account
    account = db_session.read_account_by_id(account_id=1)

    assert account.id == 1
    assert account.name == "validAccount"


def test_success_account_read_by_name(db_session, valid_account):
    _ = valid_account
    account = db_session.read_account_by_name(account_name="validAccount")

    assert account.id == 1


def test_success_account_creation(db_session, valid_user):
    _ = valid_user
    account = db_session.add_account(user_id=1, account_name="accountName")

    assert isinstance(account.id, int)
    assert account.id == 1


def test_success_account_deletion(db_session, valid_account):
    _ = valid_account
    result = db_session.delete_account(account_id=1)
    assert result == 1


def test_success_account_incomes_list(db_session, valid_income):
    _ = valid_income
    income_list = db_session.read_account_incomes(account_id=1)

    assert isinstance(income_list, list)
    assert len(income_list) > 0


#
# ERROR HANDLING
#


def test_error_account_read_by_id(db_session, valid_account):
    _ = valid_account
    user = db_session.read_account_by_id(account_id=5)

    assert user is None


def test_error_account_read_by_name(db_session, valid_account):
    _ = valid_account
    account_id = db_session.read_account_by_name(account_name="wrongAccount")

    assert account_id is None


def test_error_account_creation_invalid_user(db_session, valid_account):
    _ = valid_account
    account = db_session.add_account(user_id=20, account_name="accountName")

    assert isinstance(account, str) and "User ID does not exist" in account


def test_error_account_creation_invalid_name(db_session, valid_account):
    _ = valid_account
    account = db_session.add_account(user_id=1, account_name="validAccount")

    assert account == "Account name already exists"


def test_error_account_creation_invalid_type(db_session, valid_user):
    _ = valid_user
    account = db_session.add_account(user_id=1, account_name="validAccount", account_type="STUPID")

    assert (
        account
        == "A LookupError occurred: 'STUPID' is not among the defined enum values. Enum name: accounttypeenum. Possible values: BANK, CARD, CASH"
    )


def test_error_acccount_delete_wrong_account_id(db_session):
    result = db_session.delete_account(account_id=1)

    assert result == 0


def test_error_account_income_list_invalid_account(db_session):
    income_list = db_session.read_account_incomes(account_id=1)

    assert income_list == list()

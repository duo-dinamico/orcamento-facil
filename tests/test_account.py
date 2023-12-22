#
# DEFAULT BEHAVIOUR
#


def test_success_account_read_by_id(db_session, valid_account):
    _ = valid_account
    account = db_session.model_account.read_account_by_id(id=1)

    assert account.id == 1
    assert account.name == "validAccount"


def test_success_account_read_by_name(db_session, valid_account):
    _ = valid_account
    account = db_session.model_account.read_account_by_name(name="validAccount")

    assert account.id == 1


def test_success_account_creation(db_session, valid_user):
    _ = valid_user
    account = db_session.model_account.create_account(user_id=1, name="accountName")

    assert isinstance(account.id, int)
    assert account.id == 1


def test_success_account_deletion(db_session, valid_account):
    _ = valid_account
    result = db_session.model_account.delete_account(id=1)
    assert result == 1


def test_success_account_update(db_session, valid_account):
    _ = valid_account
    account = db_session.model_account.read_account_by_id(1)
    assert account.balance == 0
    account.balance += 100
    db_session.model_account.update_account(account)
    updated_account = db_session.model_account.read_account_by_id(1)
    assert updated_account.balance == 100


def test_success_user_accounts_list(db_session, valid_account):
    _ = valid_account
    account_list = db_session.model_account.read_accounts_by_user(user_id=1, account_type="BANK")

    assert isinstance(account_list, list)
    assert len(account_list) > 0


#
# ERROR HANDLING
#


def test_error_account_read_by_id(db_session, valid_account):
    _ = valid_account
    user = db_session.model_account.read_account_by_id(id=5)

    assert user is None


def test_error_account_read_by_name(db_session, valid_account):
    _ = valid_account
    account_id = db_session.model_account.read_account_by_name(name="wrongAccount")

    assert account_id is None


def test_error_account_creation_invalid_user(db_session, valid_account):
    _ = valid_account
    account = db_session.model_account.create_account(user_id=20, name="accountName")

    assert isinstance(account, str) and "User ID does not exist" in account


def test_error_account_creation_invalid_name(db_session, valid_account):
    _ = valid_account
    account = db_session.model_account.create_account(user_id=1, name="validAccount")

    assert account == "Account name already exists"


def test_error_account_creation_invalid_type(db_session, valid_user):
    _ = valid_user
    account = db_session.model_account.create_account(user_id=1, name="validAccount", account_type="STUPID")

    assert (
        account
        == "A LookupError occurred: 'STUPID' is not among the defined enum values. Enum name: accounttypeenum. Possible values: BANK, CARD, CASH"
    )


def test_error_acccount_delete_wrong_account_id(db_session):
    result = db_session.model_account.delete_account(id=1)

    assert result == 0


def test_error_accounts_list_invalid_user(db_session):
    account_list = db_session.model_account.read_accounts_by_user(user_id=1, account_type="BANK")

    assert account_list == list()

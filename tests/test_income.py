#
# DEFAULT BEHAVIOUR
#


def test_success_income_read_by_name(db_session, valid_income):
    _ = valid_income
    income = db_session.read_income_by_name(name="validIncome")

    assert income.id == 1
    assert income.name == "validIncome"


def test_success_income_creation(db_session, valid_account, valid_user):
    _ = valid_account
    _ = valid_user
    income = db_session.create_income(account_id=1, user_id=1, name="newIncome")

    assert isinstance(income.id, int)
    assert income.id == 1


def test_success_income_delete(db_session, valid_income):
    _ = valid_income
    result = db_session.delete_income(id=1)

    assert result == 1


#
# ERROR HANDLING
#


def test_error_income_read_by_name(db_session, valid_income):
    _ = valid_income
    income_id = db_session.read_income_by_name(name="wrongAccount")
    print("Teste")

    assert income_id is None


def test_error_income_creation_invalid_account(db_session, valid_user):
    _ = valid_user
    income = db_session.create_income(account_id=1, user_id=1, name="newIncome")

    assert income == "User ID or Account ID does not exist"


def test_error_income_creation_invalid_name(db_session, valid_income):
    _ = valid_income
    income = db_session.create_income(account_id=1, user_id=1, name="validIncome")

    assert income == "Income name already exists"


def test_error_income_delete_invalid_income(db_session):
    result = db_session.delete_income(id=1)

    assert result == 0

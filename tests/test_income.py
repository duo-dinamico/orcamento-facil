#
# DEFAULT BEHAVIOUR
#


def test_success_income_read_by_name(db_session, valid_income):
    _ = valid_income
    income = db_session.model_income.read_income_by_name(name="validIncome")

    assert income.id == 1
    assert income.name == "validIncome"


def test_success_income_creation(db_session, valid_account, valid_user):
    _ = valid_account
    _ = valid_user
    income = db_session.model_income.create_income(account_id=1, user_id=1, name="newIncome")

    assert isinstance(income.id, int)
    assert income.id == 1


def test_success_income_delete(db_session, valid_income):
    _ = valid_income
    result = db_session.model_income.delete_income(id=1)

    assert result == 1


def test_success_income_list_by_account(db_session, valid_income):
    _ = valid_income
    income_list = db_session.model_income.read_incomes_by_account(account_id=1)

    assert isinstance(income_list, list)
    assert len(income_list) > 0


def test_success_income_list_by_user(db_session, valid_income, valid_income_second):
    _ = valid_income
    _ = valid_income_second
    income_list = db_session.model_income.read_incomes_by_user(user_id=1)

    assert isinstance(income_list, list)
    assert len(income_list) == 2


#
# ERROR HANDLING
#


def test_error_income_read_by_name(db_session, valid_income):
    _ = valid_income
    income_id = db_session.model_income.read_income_by_name(name="wrongAccount")

    assert income_id is None


def test_error_income_creation_invalid_account(db_session, valid_user):
    _ = valid_user
    income = db_session.model_income.create_income(account_id=1, user_id=1, name="newIncome")

    assert income == "User ID or Account ID does not exist"


def test_error_income_creation_invalid_name(db_session, valid_income):
    _ = valid_income
    income = db_session.model_income.create_income(account_id=1, user_id=1, name="validIncome")

    assert income == "Income name already exists"


def test_error_income_delete_invalid_income(db_session):
    result = db_session.model_income.delete_income(id=1)

    assert result == 0


def test_error_income_list_invalid_account(db_session):
    income_list = db_session.model_income.read_incomes_by_account(account_id=1)

    assert income_list == list()


def test_error_income_list_invalid_user(db_session):
    income_list = db_session.model_income.read_incomes_by_user(user_id=1)

    assert income_list == list()

from ezbudget.modules.db.db_crud_income import create_income, delete_income, read_income_by_name

#
# DEFAULT BEHAVIOUR
#


def test_success_income_read_by_name(db_session, valid_income):
    _ = valid_income
    income_id = read_income_by_name(db_session, name="validIncome")

    assert income_id == 1


def test_success_income_creation(db_session, valid_account):
    _ = valid_account
    income_id = create_income(db_session, account_id=1, name="newIncome")

    assert isinstance(income_id, int)
    assert income_id == 1


def test_success_income_delete(db_session, valid_income):
    _ = valid_income
    result = delete_income(db_session, income_id=1)

    assert result is True


#
# ERROR HANDLING
#


def test_error_income_read_by_name(db_session, valid_income):
    _ = valid_income
    income_id = read_income_by_name(db_session, name="wrongAccount")
    print("Teste")

    assert income_id is None


def test_error_income_creation_invalid_account(db_session):
    income_id = create_income(db_session, account_id=1, name="newIncome")

    assert income_id is None


def test_error_income_creation_invalid_name(db_session, valid_income):
    _ = valid_income
    income_id = create_income(db_session, account_id=1, name="validIncome")

    assert income_id is None


def test_error_income_delete_invalid_income(db_session):
    result = delete_income(db_session, income_id=1)

    assert result is False

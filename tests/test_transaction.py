from datetime import datetime

#
# DEFAULT BEHAVIOUR
#


def test_success_transaction_created(db_session, valid_account, valid_subcategory):
    """Tests the success of the create_transaction method."""
    _ = valid_account
    _ = valid_subcategory
    transaction = db_session.create_transaction(
        account_id=1, subcategory_id=1, date=datetime(2022, 10, 10), value=100, description="Desc"
    )

    assert transaction.id == 1


def test_success_transaction_read_by_id(db_session, valid_transaction):
    """Tests the success of the read_transaction_by_id method."""
    _ = valid_transaction
    transaction = db_session.read_transaction_by_id(transaction_id=1)

    assert transaction.id == 1
    assert transaction.description == "validTransaction"


def test_success_transaction_read_list_by_account(db_session, valid_transaction):
    """Tests the success of the read_transaction_list_by_account method."""
    _ = valid_transaction
    transaction_list = db_session.read_transaction_list_by_account(account_id=1)

    assert type(transaction_list) is list
    assert transaction_list[0].description == "validTransaction"


def test_success_transaction_read_list_by_wrong_account(db_session, valid_subcategory):
    """Tests the return of empty list of the read_transaction_list_by_account method, when an account don't exist."""
    _ = valid_subcategory
    transaction = db_session.read_transaction_list_by_account(account_id=5)

    assert transaction == []


#
# ERROR HANDLING
#


def test_error_transaction_created(db_session, valid_subcategory):
    """Tests the error of the create_transaction method when the account or the subcategory don't exits."""
    _ = valid_subcategory
    transaction = db_session.create_transaction(
        account_id=1, subcategory_id=1, date=datetime(2023, 5, 5), value=100, description="teste"
    )

    assert transaction == "Either Account ID or SubCategory ID does not exist"


def test_error_transaction_read_by_id(db_session, valid_subcategory):
    """Tests the error of the read_transaction_by_id method when the transaction don't exit."""
    _ = valid_subcategory
    transaction = db_session.read_transaction_by_id(transaction_id=5)

    assert transaction is None

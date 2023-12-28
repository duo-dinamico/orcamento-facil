from datetime import datetime

from ezbudget.model.base_models import Transaction

#
# DEFAULT BEHAVIOUR
#


def test_success_transaction_created(db_session, valid_account, valid_subcategory):
    """Tests the success of the create_transaction method."""
    _ = valid_account
    _ = valid_subcategory
    transaction = db_session.model_transaction.create_transaction(
        account_id=1, subcategory_id=1, date=datetime(2022, 10, 10), value=100, description="Desc"
    )

    assert transaction.id == 1


def test_success_transaction_read_by_id(db_session, valid_transaction):
    """Tests the success of the read_transaction_by_id method."""
    _ = valid_transaction
    transaction = db_session.model_transaction.read_transaction_by_id(transaction_id=1)

    assert transaction.id == 1
    assert transaction.description == "validTransaction"


def test_success_transaction_read_list_by_account(db_session, valid_transaction):
    """Tests the success of the read_transaction_list_by_account method."""
    _ = valid_transaction
    transaction_list = db_session.model_transaction.read_transaction_list_by_account(account_id=1)

    assert isinstance(transaction_list, list)
    assert transaction_list[0].description == "validTransaction"


def test_success_transaction_read_list_by_wrong_account(db_session, valid_subcategory):
    """Tests the return of empty list of the read_transaction_list_by_account method, when an account don't exist."""
    _ = valid_subcategory
    transaction = db_session.model_transaction.read_transaction_list_by_account(account_id=5)

    assert transaction == []


def test_success_transaction_read_list_by_user(db_session, valid_user, valid_transaction):
    """Tests the success of the read_transaction_list_by_user method."""
    _ = valid_transaction
    _ = valid_user
    transaction_list = db_session.model_transaction.read_transaction_list_by_user(user_id=1)

    assert isinstance(transaction_list, list)
    assert transaction_list[0].description == "validTransaction"
    for transaction in transaction_list:
        assert transaction.account.user_id == 1


def test_success_transaction_updated(db_session, valid_transaction):
    """Tests the success of the update_transaction method."""
    _ = valid_transaction
    updated_data = {
        "account_id": 1,
        "subcategory_id": 1,
        "date": datetime(2022, 10, 10),
        "value": 100,
        "description": "Desc 2",
    }

    # Update the database
    updated_transaction_id = db_session.model_transaction.update_transaction(
        transaction_id=1, transaction_data=updated_data
    )
    # Read from database again
    transaction = db_session.model_transaction.read_transaction_by_id(transaction_id=updated_transaction_id)

    assert transaction.description == "Desc 2"


def test_success_transaction_delete(db_session, valid_transaction):
    """Tests the success of the delete_transaction method."""
    _ = valid_transaction
    deleted_id = db_session.model_transaction.delete_transaction(transaction_id=1)

    assert isinstance(deleted_id, int)
    assert deleted_id == 1


#
# ERROR HANDLING
#


def test_error_transaction_created(db_session, valid_subcategory):
    """Tests the error of the create_transaction method when the account or the subcategory don't exits."""
    _ = valid_subcategory
    transaction = db_session.model_transaction.create_transaction(
        account_id=1, subcategory_id=1, date=datetime(2023, 5, 5), value=100, description="teste"
    )

    assert transaction == "Either Account ID or SubCategory ID does not exist"


def test_error_transaction_read_by_id(db_session, valid_subcategory):
    """Tests the error of the read_transaction_by_id method when the transaction don't exit."""
    _ = valid_subcategory
    transaction = db_session.model_transaction.read_transaction_by_id(transaction_id=5)

    assert transaction is None


def test_error_transaction_read_list_by_user(db_session):
    """Tests error of the read_transaction_list_by_user method if the user don't exist."""

    transaction_list = db_session.model_transaction.read_transaction_list_by_user(user_id=55)

    assert isinstance(transaction_list, list)
    assert transaction_list == []


def test_error_transaction_updated_wrong_id(db_session):
    """Tests the error of the update_transaction method, if wrong id is given."""

    updated_data = {
        "account_id": 1,
        "subcategory_id": 1,
        "date": datetime(2022, 10, 10),
        "value": 100,
        "description": "Desc 2",
    }

    updated_transaction_id = db_session.model_transaction.update_transaction(
        transaction_id=1, transaction_data=updated_data
    )

    assert updated_transaction_id is None


def test_error_transaction_delete(db_session, valid_transaction):
    """Tests the error of the delete_transaction method when invalid transaction."""
    _ = valid_transaction
    deleted_id = db_session.model_transaction.delete_transaction(transaction_id=55)

    assert isinstance(deleted_id, int)
    assert deleted_id != 55

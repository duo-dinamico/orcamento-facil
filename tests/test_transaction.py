from datetime import datetime

#
# DEFAULT BEHAVIOUR
#


def test_success_transaction_read_by_id(db_session, valid_transaction):
    _ = valid_transaction
    transaction = db_session.read_transaction_by_id(1)

    assert transaction.id == 1
    assert transaction.description == "validTransaction"


def test_success_transaction_created(db_session, valid_account, valid_subcategory):
    _ = valid_account
    _ = valid_subcategory
    transaction = db_session.create_transaction(
        account_id=1, subcategory_id=1, date=datetime(2022, 10, 10), value=100, description="Desc"
    )

    assert transaction.id == 1


#
# ERROR HANDLING
#


def test_error_transaction_read_by_id(db_session, valid_subcategory):
    _ = valid_subcategory
    transaction = db_session.read_transaction_by_id(5)

    assert transaction is None


def test_error_transaction_created(db_session, valid_subcategory):
    _ = valid_subcategory
    transaction = db_session.create_transaction(
        account_id=1, subcategory_id=1, date=datetime(2023, 5, 5), value=100, description="teste"
    )

    assert transaction == "Either Account ID or SubCategory ID does not exist"

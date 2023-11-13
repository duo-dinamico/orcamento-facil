from datetime import datetime

from sqlalchemy import select

from ..utils.logging import logger
from .db_database import SessionLocal
from .db_models import Transaction
from .db_crud_account import read_account_by_id


def read_transaction_by_id(db: SessionLocal, transaction_id: int) -> Transaction | None:
    """Return a transaction object that has the given id.

    Args:
        db: database session.
        transaction_id: the transaction id.

    Returns:
        transaction: a transaction object if the transaction exist.
        None: if the transaction don't exist.
    """
    transaction = db.scalars(select(Transaction).where(Transaction.id == transaction_id)).first()
    logger.debug(f"read_transaction_by_id: {transaction}")
    if not transaction:
        return None
    return transaction


def create_transaction(
    db: SessionLocal,
    account_id: int,
    subcategory_id: int,
    date: datetime,
    value: int,
    description: str = "",
) -> int | None:
    """Create a new transaction in the database, and return the transaction id.

    Args:
        db: database session.
        account_id: the id of the account where the transaction will be created.
        subcategory_id: the id of the category of the transation.
        date: date of the transaction, in datetime format.
        value: value of the transaction in cents, positive if credit, negative if debit.
        description: short description of the transaction.

    Returns:
        trasaction id: if a new transaction was created
        None: if the transaction failed to be created.
    """

    # Check if the account id is valid
    account = read_account_by_id(db, account_id=account_id)
    if not account:
        logger.debug(f"Account don't exist: {account_id}.")
        return None

    # Check if the subcategory id is valid
    #
    #

    logger.info(f"create_transaction: {account_id} {subcategory_id} {date} {value} {description}")

    # Add account to the database
    db_transaction = Transaction(
        account_id=account_id,
        subcategory_id=subcategory_id,
        date=date,
        value=value,
        description=description,
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction.id

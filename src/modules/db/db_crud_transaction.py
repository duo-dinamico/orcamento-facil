from datetime import datetime

from sqlalchemy import select

from ..utils.logging import logger
from .db_database import SessionLocal
from .db_models import Transaction


def create_transaction(
    db: SessionLocal,
    account_id: int,
    subcategory_id: int,
    date: datetime,
    value: int,
    description: str = "",
) -> int:
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

    pass

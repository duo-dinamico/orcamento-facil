from sqlalchemy import select

from ..utils.hash import get_hashed_password, verify_password
from ..utils.logging import logger
from .db_crud_user import read_user_by_id
from .db_database import SessionLocal
from .db_models import Account, AccountTypeEnum, User


def read_account_by_id(db: SessionLocal, account_id: str) -> Account:
    """Return an account object that has the given id.

    Args:
        db: database session.
        account_id: the account id.

    Returns:
        account: if the account exist.
        None: if the account don't exist.
    """
    account = db.scalars(select(Account).where(Account.id == account_id)).first()
    logger.info(f"read_account_by_id: {account}")
    if not account:
        return None
    return account


def read_account_by_name(db: SessionLocal, account_name: str) -> int:
    """Return an account id that has the given name.

    Args:
        db: database session.
        account_name: the account name.

    Returns:
        account id: if the account exist.
        None: if the account don't exist.
    """
    account = db.scalars(select(Account).where(Account.name == account_name)).first()
    logger.info(f"read_account_by_name: {account}")
    if not account:
        return None
    return account.id


def create_account(
    db: SessionLocal,
    account_name: str,
    user_id: int,
    initial_balance: int = 0,
    account_type: AccountTypeEnum = "BANK",
    currency: str = "EUR",
) -> Account.id:
    """Create a new account in the database, for a given user and return the new account id.

    Args:
        db: database session.
        account_name: the name of the account, that must be unique.
        user_id: user id that own the account.

    Returns:
        account id: if a new account was created
        None: if the user_id is not valid or if the account name already exists
    """

    # Check if the user id is valid
    user = read_user_by_id(db, id=user_id)
    if not user:
        logger.info(f"User don't exist: {user_id}.")
        return None

    # Check if the account name already exist
    account = read_account_by_name(db, account_name)
    if account:
        logger.info(f"Account already exist: {account_name}.")
        return None
    logger.info(
        f"create_account: {user_id} {account_name} {account_type} {currency} {initial_balance}"
    )

    # Check if type is valid
    if account_type not in AccountTypeEnum.__members__:
        logger.info(f"Account type don't exist: {account_type}.")
        return None

    # Add account to the database
    db_account = Account(
        user_id=user_id,
        name=account_name,
        account_type=account_type,
        currency=currency,
        initial_balance=initial_balance,
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account.id


def delete_account(db: SessionLocal, account_id: int, user_id: int) -> bool:
    """Delete an account in the database.

    Args:
        db: database session.
        account_id: id of the account to delete.
        user_id: id of the loggeg in user.

    Returns:
        True: if deleted.
        False: if not deleted.
    """

    # Get the account checking the id's of the account and user
    account = db.scalars(
        select(Account).where(Account.id == account_id, Account.user_id == user_id)
    ).first()
    if not account:
        return False

    else:
        # Delete the account
        delete_result = db.delete(account)
        db.commit()

        return True

from sqlalchemy import select

from ezbudget.model import Account, AccountTypeEnum, Income, Model

from .db_crud_user import read_user_by_id

db = Model()


def read_account_by_id(db: db.session, account_id: str) -> Account:
    """Return an account object that has the given id.

    Args:
        db: database session.
        account_id: the account id.

    Returns:
        account: if the account exist.
        None: if the account don't exist.
    """
    account = db.scalars(select(Account).where(Account.id == account_id)).first()
    if not account:
        return None
    return account


def read_account_by_name(db: db.session, account_name: str) -> int:
    """Return an account id that has the given name.

    Args:
        db: database session.
        account_name: the account name.

    Returns:
        account_id: if the account exist.
        None: if the account don't exist.
    """
    account = db.scalars(select(Account).where(Account.name == account_name)).first()
    if not account:
        return None
    return account.id


def create_account(
    db: db.session,
    account_name: str,
    user_id: int,
    initial_balance: int = 0,
    account_type: AccountTypeEnum = "BANK",
    currency: str = "EUR",
) -> int:
    """Create a new account in the database, for a given user and return the new account id.

    Args:
        db: database session.
        account_name: the name of the account, that must be unique.
        user_id: user id that own the account.
        initial_balance: the initial balance of the account, it's zero by default
        account_type: the type of the account, it's BANK by default
        currency: the currency of the account, it's EUR by default

    Returns:
        account_id: if a new account was created
        None: if the user_id is not valid or if the account name already exists
    """

    # Check if the user id is valid
    user = read_user_by_id(db, id=user_id)
    if not user:
        return None

    # Check if the account name already exist
    account = read_account_by_name(db, account_name)
    if account:
        return None

    # Check if type is valid
    if account_type not in AccountTypeEnum.__members__:
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


def delete_account(db: db.session, account_id: int, user_id: int) -> bool:
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
    account = db.scalars(select(Account).where(Account.id == account_id, Account.user_id == user_id)).first()
    if not account:
        return False

    else:
        # Delete the account
        db.delete(account)
        db.commit()

        return True


def read_account_incomes(db: db.session, account_id: int) -> list:
    """Return a list of account incomes.

    Args:
        db: database session.
        account_id: user id owner of the accounts.

    Returns:
        income_list: list of the account incomes
        None: if the account_id is not valid
    """

    # Check if the account_id is valid
    account = read_account_by_id(db, account_id)
    if not account:
        return None

    # get the list of income
    income_list = db.scalars(select(Income).where(Income.account_id == account_id)).all()
    return income_list

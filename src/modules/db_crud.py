from sqlalchemy import select

from modules.db_database import SessionLocal
from modules.db_models import User, Account, AccountTypeEnum
from modules.utils import get_hashed_password, verify_password


#
# User
#


def read_user_by_name(db: SessionLocal, username: str) -> User:
    """Return a user object that has the given username.

    Args:
        db: database session.
        username: the username of the user.

    Returns:
        user: if the user exist.
        None: if the username don't exist.
    """
    user = db.scalars(select(User).where(User.username == username)).first()
    print(f"read_user_by_name: {user}")
    if not user:
        return None
    return user


def read_user_by_id(db: SessionLocal, id: int) -> User:
    """Return a user object that has the given id.

    Args:
        db: database session.
        id: the id of the user.

    Returns:
        user: if the user id exist.
        None: if the id don't exist.
    """
    user = db.scalars(select(User).where(User.id == id)).first()
    print(f"read_user_by_id: {user}")
    if not user:
        return None
    return user


def create_user(db: SessionLocal, username: str, user_password: str) -> User.id:
    """Create a new user in the database, and return the his id.

    Args:
        db: database session.
        username: the username of the user.
        user_passord: the password of the user.

    Returns:
        user id: if a new user was created
        None: if the username already exists
    """

    # Check if the username already exist
    user = read_user_by_name(db, username)
    print(f"create user: user {user}")
    if user:
        print(f"User already exist: {username}, {user.id}")
        return None

    # Crypt the password
    hashed_password = get_hashed_password(user_password)

    # Add user to the database
    db_user = User(username=username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print(f"create_user: {db_user.id}")
    return db_user.id


def login_user(db: SessionLocal, username: str, user_password: str) -> User.id:
    """Return the id of the user, if the password is correct.

    Args:
        db: database session.
        username: the username of the user.
        user_passord: the password of the user.

    Returns:
        Returns the id of the user that is logging in.

    """
    user = read_user_by_name(db, username)
    print(f"login_user: user {user}")

    if user == None or not verify_password(user_password, user.password):
        return None

    else:
        return user.id


#
# Account
#


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
    print(f"read_account_by_id: {account}")
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
    print(f"read_account_by_name: {account_name}")
    account = db.scalars(select(Account).where(Account.name == account_name)).first()
    print(f"read_account_by_name: {account}")
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
        return None

    # Check if the account name already exist
    account = read_account_by_name(db, account_name)
    print(f"create_account: account {account} -> {account_name}")
    if account:
        print(f"Account already exist: {account_name}, {account}")
        return None
    print(f"create_account: {user_id} {account_name} {account_type} {currency} {initial_balance}")
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


def read_user_accounts(db: SessionLocal, user_id: int) -> list:
    """Return a list of user accounts.

    Args:
        db: database session.
        user_id: user id owner of the accounts.

    Returns:
        account_list: list of the user accounts
        None: if the user_id is not valid
    """

    # Check if the user id is valid
    user = read_user_by_id(db, user_id)
    if not user:
        return None

    # get the list of accounts
    account_list = db.scalars(select(Account).where(Account.user_id == user_id)).all()
    return account_list


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

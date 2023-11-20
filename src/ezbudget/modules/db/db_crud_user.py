from sqlalchemy import select

from ezbudget.model import Account, Income, Model, User
from ezbudget.utils import get_hashed_password, verify_password

db = Model()


def read_user_by_name(db: db.session, username: str) -> User:
    """Return a user object that has the given username.

    Args:
        db: database session.
        username: the username of the user.

    Returns:
        user: if the user exist.
        None: if the username don't exist.
    """

    user = db.scalars(select(User).where(User.username == username)).first()
    if not user:
        return None
    return user


def read_user_by_id(db: db.session, id: int) -> User:
    """Return a user object that has the given id.

    Args:
        db: database session.
        id: the id of the user.

    Returns:
        user: if the user id exist.
        None: if the id don't exist.
    """

    user = db.scalars(select(User).where(User.id == id)).first()
    if not user:
        return None
    return user


def create_user(db: db.session, username: str, user_password: str) -> int:
    """Create a new user in the database, and return the id.

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
    if user:
        return None

    # Crypt the password
    hashed_password = get_hashed_password(user_password)

    # Add user to the database
    db_user = User(username=username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user.id


def login_user(db: db.session, username: str, user_password: str) -> int:
    """Return the id of the user, if the password is correct.

    Args:
        db: database session.
        username: the username of the user.
        user_passord: the password of the user.

    Returns:
        Returns the id of the user that is logging in.
    """

    user = read_user_by_name(db, username)

    if user is None or not verify_password(user_password, user.password):
        return None

    else:
        return user.id


def read_user_accounts(db: db.session, user_id: int) -> list:
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

    # get the list of accounts id's
    accounts_list = db.scalars(select(Account).where(Account.user_id == user_id)).all()
    return accounts_list


def read_user_incomes(db: db.session, user_id: int) -> list:
    """Return a list of incomes, from a given user.

    Args:
        db: database session.
        user_id: user id owner of the accounts.

    Returns:
        income_list: list of the user incomes
        None: if the user_id is not valid
    """

    # Check if the user_id is valid
    account = read_user_by_id(db, user_id)
    if not account:
        return None

    # get the list of accounts of the user
    account_list = read_user_accounts(db, user_id=user_id)
    account_list_id = []
    for acc in account_list:
        account_list_id.append(acc.id)

    # Get the list of all incomes
    income_list_all = db.scalars(select(Income)).all()

    income_list = []

    for inc in income_list_all:
        if inc.account_id in account_list_id:
            income_list.append(inc)

    # get the list of income
    return income_list

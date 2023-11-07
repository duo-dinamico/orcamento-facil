from sqlalchemy import select

from ..utils.hash import get_hashed_password, verify_password
from ..utils.logging import logger
from .db_database import SessionLocal
from .db_models import Account, AccountTypeEnum, User


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
    logger.info(f"read_user_by_name: {user}")
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
    logger.info(f"read_user_by_id: {user}")
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
    logger.info(f"create user: user {user}")
    if user:
        return None

    # Crypt the password
    hashed_password = get_hashed_password(user_password)

    # Add user to the database
    db_user = User(username=username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"create_user: {db_user.id}")
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
    logger.info(f"login_user: user {user}")

    if user == None or not verify_password(user_password, user.password):
        return None

    else:
        return user.id


#
# Account
#


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

    # get the list of accounts id's
    accounts_list = db.scalars(select(Account).where(Account.user_id == user_id)).all()
    logger.info(f"List of accounts: {accounts_list}")
    return accounts_list

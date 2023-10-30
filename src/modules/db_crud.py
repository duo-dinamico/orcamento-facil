from sqlalchemy import select

from modules.db_database import SessionLocal
from modules.db_models import User
from modules.utils import get_hashed_password, verify_password


def read_user(db: SessionLocal, username: str) -> User:
    """Return a user object that has the given username.

    Args:
        db: database session.
        username: the username of the user.

    Returns:
        user: if the user exist.
        None: if the username don't exist.
    """
    user = db.scalars(select(User).where(User.username == username)).first()
    print(f"read_user: {user}")
    if not user:
        return None
    return user


def create_user(db: SessionLocal, username: str, user_password: str) -> User:
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
    user = read_user(db, username)
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


def login_user(db: SessionLocal, username: str, user_password: str) -> User:
    """Return the id of the user, if the password is correct.

    Args:
        db: database session.
        username: the username of the user.
        user_passord: the password of the user.

    Returns:
        Returns the id of the user that is logging in.

    """
    user = read_user(db, username)
    print(f"login_user: user {user}")

    if user == None or not verify_password(user_password, user.password):
        return None

    else:
        return user.id

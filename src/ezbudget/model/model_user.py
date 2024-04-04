from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from ezbudget.model import User


class ModelUser:
    def __init__(self, parent_model):
        self.parent = parent_model

    def create_user(self, username: str, password: str, personal_key: bytes) -> User | str:
        """Create a new user in the database, and return the id.

        Args:
            username: the username of the user.
            password: the password of the user.

        Returns:
            user: if a new user was created
            None: if the username already exists
        """
        try:
            user = User(username=username, password=password, personal_key=personal_key)
            self.parent.session.add(user)
            self.parent.session.commit()
            self.parent.session.refresh(user)

            return user
        except IntegrityError:
            self.parent.session.rollback()
            return "User already exists"

    def read_user_by_name(self, username: str) -> User | None:
        """Return a user object that has the given username.

        Args:
            username: the username of the user.

        Returns:
            User: if the user exist.
            None: if the username doesn't exist.
        """
        return self.parent.read_first_basequery(select(User).where(User.username == username))

    def read_user_by_id(self, id: int) -> User | None:
        """Return a user object that has the given id.

        Args:
            id: the id of the user.

        Returns:
            User: if the user exist.
            None: if the id doesn't exist.
        """
        return self.parent.read_first_basequery(select(User).where(User.id == id))

    def read_users(self) -> list:
        return self.parent.read_all_basequery(select(User))

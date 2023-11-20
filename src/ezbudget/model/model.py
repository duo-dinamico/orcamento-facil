from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from ezbudget.model import Account, AccountTypeEnum, Base, User


class Model:
    def __init__(self) -> None:
        engine = create_engine("sqlite:///of.db")
        session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        Base.metadata.create_all(engine)
        self.session = session_local()

        self.user = None

    def add_user(self, username: str, password: str = "") -> User | None:
        """Create a new user in the database, and return the id.

        Args:
            username: the username of the user.
            password: the password of the user.

        Returns:
            user: if a new user was created
            None: if the username already exists
        """
        user = User(username=username, password=password)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user

    def read_user_by_name(self, username: str) -> User | None:
        """Return a user object that has the given username.

        Args:
            username: the username of the user.

        Returns:
            User: if the user exist.
            None: if the username don't exist.
        """
        user = self.session.scalars(select(User).where(User.username == username)).first()
        return user

    def add_account(
        self,
        account_name: str,
        user_id: int,
        initial_balance: int = 0,
        account_type: AccountTypeEnum = "BANK",
        currency: str = "EUR",
    ) -> Account | None:
        """Create a new account in the database, for a given user and return the new account id.

        Args:
            account_name: the name of the account, that must be unique.
            user_id: user id that own the account.
            initial_balance: the initial balance of the account, it's zero by default
            account_type: the type of the account, it's BANK by default
            currency: the currency of the account, it's EUR by default

        Returns:
            Account: if a new account was created
            None: if the user_id is not valid or if the account name already exists
        """
        account = Account(
            user_id=user_id,
            name=account_name,
            account_type=account_type,
            currency=currency,
            initial_balance=initial_balance,
        )

        self.session.add(account)
        self.session.commit()
        self.session.refresh(account)
        return account

    def read_account_by_name(self, account_name: str) -> Account | None:
        """Return an account id that has the given name.

        Args:
            account_name: the account name.

        Returns:
            account_id: if the account exist.
            None: if the account don't exist.
        """
        account = self.session.scalars(select(Account).where(Account.name == account_name)).first()
        return account

    def read_accounts_by_user(self, user_id: int) -> list:
        """Return a list of user accounts.

        Args:
            user_id: user id owner of the accounts.

        Returns:
            account_list: list of the user accounts
            None: if the user_id is not valid
        """
        accounts_list = self.session.scalars(select(Account).where(Account.user_id == user_id)).all()
        return accounts_list

    def read_account_by_id(self, account_id: str) -> Account | None:
        """Return an account object that has the given id.

        Args:
            account_id: the account id.

        Returns:
            Account: if the account exist.
            None: if the account doesn't exist.
        """
        account = self.session.scalars(select(Account).where(Account.id == account_id)).first()
        return account

from sqlalchemy import and_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from ezbudget.model import Account, AccountTypeEnum


class ModelAccount:
    def __init__(self, parent_model):
        self.parent = parent_model

    def create_account(
        self,
        user_id: int,
        name: str,
        account_type: AccountTypeEnum = "BANK",
        currency: str = "EUR",
        balance: int = 0,
        credit_limit: int = 0,
        payment_day: str = "",
        interest_rate: float = 0.0,
        credit_method: str = "",
    ) -> Account | None:
        """Create a new account in the database, for a given user and return the new account id.

        Args:
            user_id: user id that own the account, which must exist in the users table.
            name: the name of the account, that must be unique.
            balance: the balance of the account, it's zero by default
            account_type: the type of the account, it's BANK by default
            currency: the currency of the account, it's EUR by default

        Returns:
            Account: if a new account was created
            None: if the user_id is not valid or if the account name already exists
        """
        try:
            new_account = Account(
                user_id=user_id,
                name=name,
                account_type=account_type,
                currency=currency,
                balance=balance,
                credit_limit=credit_limit,
                payment_day=payment_day,
                interest_rate=interest_rate,
                credit_method=credit_method,
            )

            self.parent.session.add(new_account)
            self.parent.session.commit()
            self.parent.session.refresh(new_account)
            return new_account
        except IntegrityError as e:
            self.parent.session.rollback()
            if "foreign key constraint" in str(e.orig).lower():
                return "User ID does not exist"
            elif "unique constraint" in str(e.orig).lower():
                return "Account name already exists"
            else:
                return "An unknown IntegrityError occurred"
        except LookupError as lookup_error:
            self.parent.session.rollback()
            return f"A LookupError occurred: {lookup_error}"

    def read_account_by_id(self, id: int) -> Account | None:
        """Return an account object that has the given id.

        Args:
            account_id: the account id.

        Returns:
            Account: if the account exist.
            None: if the account doesn't exist.
        """
        try:
            return self.parent.read_first_basequery(select(Account).where(Account.id == id))
        except NoResultFound:
            return None

    def read_account_by_name(self, name: str) -> Account | None:
        """Return an account that has the given name.

        Args:
            name: the account name.
            account_type: type of account from the enum

        Returns:
            account: if the account exist.
            None: if the account don't exist.
        """
        try:
            return self.parent.read_first_basequery(select(Account).where(Account.name == name))
        except NoResultFound:
            return None

    def read_accounts_by_user(self, user_id: int, account_type: str) -> list:
        """Return a list of user accounts.

        Args:
            user_id: user id owner of the accounts.
            account_type: type of account from the enum

        Returns:
            account_list: list of the user accounts
        """
        try:
            return self.parent.read_all_basequery(
                select(Account).where(and_(Account.user_id == user_id), (Account.account_type == account_type))
            )
        except NoResultFound:
            return []

    def update_account(self, account: Account) -> None:
        """Update an account

        Args:
            account: the account to update.

        Returns:
            None: returns nothing
        """
        try:
            self.parent.session.add(account)
            self.parent.session.commit()
            self.parent.session.refresh(account)
        except NoResultFound:
            return False

    def delete_account(self, id: int) -> int:
        """Delete an account in the database.

        Args:
            id: id of the account to delete.

        Returns:
            deleted_row: returns the number of rows affected. 0 if none was deleted
        """
        # TODO Delete and update are under consideration due to the risk of permanent changes
        deleted_row = self.parent.session.query(Account).where(Account.id == id).delete()
        self.parent.session.commit()
        return deleted_row

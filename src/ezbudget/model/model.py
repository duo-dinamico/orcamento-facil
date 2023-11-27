from ast import List
from datetime import datetime
from typing import Optional

from sqlalchemy import and_, create_engine, event, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.query import Query
from sqlalchemy.sql.expression import ScalarSelect

from ezbudget.model import (
    Account,
    AccountTypeEnum,
    Base,
    Category,
    Income,
    MonthEnum,
    RecurrenceEnum,
    SubCategory,
    Transaction,
    User,
)


class Model:
    def __init__(self, database_name: str = "of") -> None:
        self.engine = create_engine(f"sqlite:///{database_name}.db")

        @event.listens_for(self.engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            _ = connection_record
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON;")
            cursor.close()

        session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        Base.metadata.create_all(self.engine)
        self.session = session_local()

        self.user = None

    def close_session(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)

    # GENERIC METHODS
    def read_first_basequery(self, query: Query) -> Optional[ScalarSelect]:
        """Return a SQLAlchemy query selection that matches the given query.

        Args:
            query: SQLAlchemy query object

        Returns:
            ScalarSelect: the result of the selection
        """
        return self.session.scalars(query).first()

    def read_all_basequery(self, query: Query) -> Optional[ScalarSelect]:
        """Return a SQLAlchemy query selection that matches the given query.

        Args:
            query: SQLAlchemy query object

        Returns:
            ScalarSelect: the lest with results of the selection

        """
        return self.session.scalars(query).all()

    # USER MODELS
    def create_user(self, username: str, password: str = "") -> User | None:
        """Create a new user in the database, and return the id.

        Args:
            username: the username of the user.
            password: the password of the user.

        Returns:
            user: if a new user was created
            None: if the username already exists
        """
        try:
            user = User(username=username, password=password)
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)

            return user
        except IntegrityError:
            return "User already exists"

    def read_user_by_name(self, username: str) -> User | None:
        """Return a user object that has the given username.

        Args:
            username: the username of the user.

        Returns:
            User: if the user exist.
            None: if the username doesn't exist.
        """
        try:
            return self.read_first_basequery(select(User).where(User.username == username))
        except NoResultFound:
            return None

    def read_user_by_id(self, id: int) -> User | None:
        """Return a user object that has the given id.

        Args:
            id: the id of the user.

        Returns:
            User: if the user exist.
            None: if the id doesn't exist.
        """
        try:
            return self.read_first_basequery(select(User).where(User.id == id))
        except NoResultFound:
            return None

    # ACCOUNT MODELS
    def create_account(
        self,
        user_id: int,
        name: str,
        account_type: AccountTypeEnum = "BANK",
        currency: str = "EUR",
        initial_balance: int = 0,
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
            initial_balance: the initial balance of the account, it's zero by default
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
                initial_balance=initial_balance,
                balance=balance,
                credit_limit=credit_limit,
                payment_day=payment_day,
                interest_rate=interest_rate,
                credit_method=credit_method,
            )

            self.session.add(new_account)
            self.session.commit()
            self.session.refresh(new_account)
            return new_account
        except IntegrityError as e:
            if "foreign key constraint" in str(e.orig).lower():
                return "User ID does not exist"
            elif "unique constraint" in str(e.orig).lower():
                return "Account name already exists"
            else:
                return "An unknown IntegrityError occurred"
        except LookupError as lookup_error:
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
            return self.read_first_basequery(select(Account).where(Account.id == id))
        except NoResultFound:
            return None

    def read_account_by_name(self, name: str) -> Account | None:
        """Return an account that has the given name.

        Args:
            name: the account name.

        Returns:
            account: if the account exist.
            None: if the account don't exist.
        """
        try:
            return self.read_first_basequery(select(Account).where(Account.name == name))
        except NoResultFound:
            return None

    def read_accounts_by_user(self, user_id: int, account_type: str) -> list:
        """Return a list of user accounts.

        Args:
            user_id: user id owner of the accounts.

        Returns:
            account_list: list of the user accounts
        """
        try:
            return self.read_all_basequery(
                select(Account).where(and_(Account.user_id == user_id), (Account.account_type == account_type))
            )
        except NoResultFound:
            return []

    def delete_account(self, id: int) -> int:
        """Delete an account in the database.

        Args:
            id: id of the account to delete.

        Returns:
            deleted_row: returns the number of rows affected. 0 if none was deleted
        """
        # TODO Delete and update are under consideration due to the risk of permanent changes
        deleted_row = self.session.query(Account).where(Account.id == id).delete()
        self.session.commit()
        return deleted_row

    # INCOME MODELS
    def create_income(
        self,
        user_id: int,
        account_id: int,
        name: str,
        expected_income_value: int = 0,
        real_income_value: int = 0,
        income_day: str = "1",
        income_month: MonthEnum = MonthEnum.JANUARY,
        recurrence: RecurrenceEnum = RecurrenceEnum.ONE,
    ) -> Income:
        """Create a new income, for a given account and return the new income.

        Args:
            account_id: the account id for the income.
            name: name of the income.
            expected_income_value: expected value of the income in cents, it's zero by default.
            real_income_value: real value of the income in cents, it's zero by default.
            income_day: the day of the month of the first income, it's 1 by default.
            income_month: the month of the income, from an enum.
            recurrence: recurrence of the income, from an enum, it's ONE by default.

        Returns:
            Income: The newly created income.
        """

        # Add income to the database
        try:
            income = Income(
                user_id=user_id,
                account_id=account_id,
                name=name,
                expected_income_value=expected_income_value,
                real_income_value=real_income_value,
                income_day=income_day,
                income_month=income_month,
                recurrence=recurrence,
            )
            self.session.add(income)
            self.session.commit()
            self.session.refresh(income)
            return income
        except IntegrityError as e:
            if "foreign key constraint" in str(e.orig).lower():
                return "User ID or Account ID does not exist"
            elif "unique constraint" in str(e.orig).lower():
                return "Income name already exists"
            else:
                return "An unknown IntegrityError occurred"
        except LookupError as lookup_error:
            return f"A LookupError occurred: {lookup_error}"

    def read_income_by_name(self, name: str) -> Income | None:
        """Return an income that has the given name.

        Args:
            name: the income name.

        Returns:
            income: if the income exist.
            None: if the income does not exist.
        """
        try:
            return self.read_first_basequery(select(Income).where(Income.name == name))
        except NoResultFound:
            return None

    def read_incomes_by_user(self, user_id: int) -> list:
        """Return a list of incomes from the selected user.

        Args:
            user_id: user id owner of the incomes.

        Returns:
            income_list: list of the user incomes
        """
        try:
            return self.read_all_basequery(select(Income).where(Income.user_id == user_id))
        except NoResultFound:
            return []

    def read_incomes_by_account(self, account_id: int) -> list:
        """Return a list of incomes from the selected account.

        Args:
            account_id: account owner of the incomes.

        Returns:
            income_list: list of the account incomes
        """
        try:
            return self.read_all_basequery(select(Income).where(Income.account_id == account_id))
        except NoResultFound:
            return []

    def delete_income(self, id: int) -> int:
        """Delete an income in the database.

        Args:
            db: database session.
            income_id: id of the income to delete.

        Returns:
            deleted_row: returns the number of rows affected. 0 if none was deleted

        """
        # TODO Delete and update are under consideration due to the risk of permanent changes
        deleted_row = self.session.query(Income).where(Income.id == id).delete()
        self.session.commit()
        return deleted_row

    # CATEGORY MODELS
    def create_category(self, name: str) -> Category | None:
        """Create a new category in the database, and return the category.

        Args:
            name: name of the new category.

        Returns:
            category: if a new category was created
            None: if the category failed to be created.
        """
        try:
            category = Category(name=name)
            self.session.add(category)
            self.session.commit()
            self.session.refresh(category)

            return category
        except IntegrityError:
            return "Category already exists"

    def read_category_by_name(self, name: str) -> Category | None:
        """Return a category id that has the given name.

        Args:
            name: the category name.

        Returns:
            category: if the category exist.
            None: if the category don't exist.
        """
        try:
            return self.read_first_basequery(select(Category).where(Category.name == name))
        except NoResultFound:
            return None

    def read_category_by_id(self, id: int) -> Category | None:
        """Return a category object that has the given category id.

        Args:
            id: the category id.

        Returns:
            category: category object, if the category exist.
            None: if the category does not exist.
        """
        try:
            return self.read_first_basequery(select(Category).where(Category.id == id))
        except NoResultFound:
            return None

    def read_categories(self) -> list:
        """Return a list of all categories.

        Returns:
            category_list: list of all categories.
        """
        return self.read_all_basequery(select(Category))

    # SUBCATEGORY MODELS
    def create_subcategory(
        self,
        category_id: int,
        name: str,
        recurrent: bool = False,
        recurrence: RecurrenceEnum = "ONE",
        include: bool = True,
    ) -> SubCategory | None:
        """Create a new subcategory in the database, and return the subcategory.

        Args:
            name: name of the new subcategory.

        Returns:
            subcategory: if a new subcategory was created
            None: if the subcategory failed to be created.
        """
        try:
            new_subcategory = SubCategory(
                category_id=category_id,
                name=name,
                recurrent=recurrent,
                recurrence=recurrence,
                include=include,
            )

            self.session.add(new_subcategory)
            self.session.commit()
            self.session.refresh(new_subcategory)
            return new_subcategory
        except IntegrityError as e:
            if "foreign key constraint" in str(e.orig).lower():
                return "Category ID does not exist"
            elif "unique constraint" in str(e.orig).lower():
                return "SubCategory name already exists"
            else:
                return "An unknown IntegrityError occurred"
        except LookupError as lookup_error:
            return f"A LookupError occurred: {lookup_error}"

    def read_subcategory_by_name(self, name: str) -> SubCategory | None:
        """Return a subcategory id that has the given subcategory name.

        Args:
            name: the subcategory name.

        Returns:
            subcategory: if the subcategory exist.
            None: if the subcategory don't exist.
        """
        try:
            return self.read_first_basequery(select(SubCategory).where(SubCategory.name == name))
        except NoResultFound:
            return None

    def read_subcategories_by_category_id(self, category_id: int) -> list:
        """Return a list of all subcategories from a given category id.

        Args:
            category_id: category id from where we get the subcategories list

        Returns:
            subcategory_list: list of all subcategories for a given category id, if there is at least one subcategory.
        """
        try:
            return self.read_all_basequery(select(SubCategory).where(SubCategory.category_id == category_id))
        except NoResultFound:
            return []

    #
    # TRANSACTION MODELS
    #
    def create_transaction(
        self,
        account_id: int,
        subcategory_id: int,
        date: datetime,
        value: int,
        description: str = "",
    ) -> int | None:
        """Create a new transaction in the database, and return the transaction id.

        Args:
            account_id: the id of the account where the transaction will be created.
            subcategory_id: the id of the category of the transation.
            date: date of the transaction, in datetime format.
            value: value of the transaction in cents, positive if credit, negative if debit.
            description: short description of the transaction.

        Returns:
            trasaction id: if a new transaction was created
            None: if the transaction failed to be created.
        """
        try:
            new_transaction = Transaction(
                account_id=account_id,
                subcategory_id=subcategory_id,
                date=date,
                value=value,
                description=description,
            )

            self.session.add(new_transaction)
            self.session.commit()
            self.session.refresh(new_transaction)
            return new_transaction
        except IntegrityError as e:
            if "foreign key constraint" in str(e.orig).lower():
                return "Either Account ID or SubCategory ID does not exist"
            else:
                return "An unknown IntegrityError occurred"
        except LookupError as lookup_error:
            return f"A LookupError occurred: {lookup_error}"

    def read_transaction_by_id(self, transaction_id: int) -> Transaction | None:
        """Return a transaction object that has the given id.

        Args:
            transaction_id: the transaction id.

        Returns:
            transaction: a transaction object if the transaction exist.
            None: if the transaction don't exist.
        """
        try:
            return self.read_first_basequery(select(Transaction).where(Transaction.id == transaction_id))
        except NoResultFound:
            return None

    def read_transaction_list_by_account(self, account_id: int) -> List:
        """Return a list of transactions objects that has the given account_id.

        Args:
            account_id: the account id.

        Returns:
            transaction_list: a list of transactions object if the account exist.
            []: empty list if no transaction with that account.
        """
        try:
            return self.read_all_basequery(select(Transaction).where(Transaction.account_id == account_id))
        except NoResultFound:
            return None

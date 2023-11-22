from datetime import datetime

from sqlalchemy import create_engine, event, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

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
        try:
            return self.session.scalars(select(User).where(User.username == username)).first()
        except NoResultFound:
            return None

    def add_account(
        self,
        account_name: str,
        user_id: int,
        initial_balance: int = 0,
        account_type: AccountTypeEnum = "BANK",
        currency: str = "EUR",
        credit_limit: int = 0,
        payment_day: str = "",
        interest_rate: float = 0.0,
        credit_method: str = "",
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
        try:
            new_account = Account(
                user_id=user_id,
                name=account_name,
                account_type=account_type,
                currency=currency,
                initial_balance=initial_balance,
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

    def read_account_by_name(self, account_name: str) -> Account | None:
        """Return an account that has the given name.

        Args:
            account_name: the account name.

        Returns:
            account_id: if the account exist.
            None: if the account don't exist.
        """
        try:
            return self.session.scalars(select(Account).where(Account.name == account_name)).first()
        except NoResultFound:
            return None

    def read_accounts_by_user(self, user_id: int) -> list:
        """Return a list of user accounts.

        Args:
            user_id: user id owner of the accounts.

        Returns:
            account_list: list of the user accounts
        """
        try:
            return self.session.scalars(select(Account).where(Account.user_id == user_id)).all()
        except NoResultFound:
            return None

    def read_accounts(self, query) -> list:
        """Return a list of accounts that matches the given query.

        Args:
            query: SQLAlchemy query object

        Returns:
            account_list: list of the user accounts
        """
        accounts_list = self.session.scalars(query).all()
        return accounts_list

    def read_incomes_by_name(self, user_id: int) -> list:
        """Return a list incomes from the selected user.

        Args:
            user_id: user id owner of the incomes.

        Returns:
            income_list: list of the user incomes
        """
        income_list = self.session.scalars(select(Income).where(Income.user_id == user_id)).all()
        return income_list

    def read_account_by_id(self, account_id: str) -> Account | None:
        """Return an account object that has the given id.

        Args:
            account_id: the account id.

        Returns:
            Account: if the account exist.
            None: if the account doesn't exist.
        """
        try:
            return self.session.scalars(select(Account).where(Account.id == account_id)).first()
        except NoResultFound:
            return None

    def add_income(
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

    # TODO from here down these models need to be reviewed
    def delete_account(self, account_id: int) -> bool:
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
        deleted_row = self.session.query(Account).filter(Account.id == account_id).delete()
        self.session.commit()
        # Returns affected rows. It will return 0 for no lines deleted and x for the amount of numbers deleted
        return deleted_row

    def read_account_incomes(self, account_id: int) -> list:
        """Return a list of account incomes.

        Args:
            db: database session.
            account_id: user id owner of the accounts.

        Returns:
            income_list: list of the account incomes
            None: if the account_id is not valid
        """

        # get the list of income
        income_list = self.session.scalars(select(Income).where(Income.account_id == account_id)).all()
        return income_list

    def read_category_by_name(self, name: str) -> int:
        """Return a category id that has the given name.

        Args:
            db: database session.
            name: the category name.

        Returns:
            category_id: if the category exist.
            None: if the category don't exist.
        """
        category = self.session.scalars(select(Category).where(Category.name == name)).first()
        if not category:
            return None
        return category.id

    def read_category_by_id(self, category_id: int) -> Category:
        """Return a category object that has the given category id.

        Args:
            db: database session.
            category_id: the category id.

        Returns:
            category: category object, if the category exist.
            None: if the category don't exist.
        """
        category = self.session.scalars(select(Category).where(Category.id == category_id)).first()
        if not category:
            return None
        return category

    def read_category_list(self) -> list:
        """Return a list of all categories.

        Args:
            db: database session.

        Returns:
            category_list: list of all categories, if there is at least one category.
            None: if there is no category.
        """
        category_list = self.session.scalars(select(Category)).all()
        if len(category_list) == 0:
            return None
        return category_list

    def add_category(self, name: str) -> int:
        """Create a new category in the database, and return the category id.

        Args:
            db: database session.
            name: name of the new category.

        Returns:
            category_id: if a new category was created
            None: if the category failed to be created.
        """
        # Check if name already exist
        category = self.read_category_by_name(name=name)
        if category:
            return None

        # Add category to the database
        db_category = Category(name=name)
        self.session.add(db_category)
        self.session.commit()
        self.session.refresh(db_category)
        return db_category.id

    def read_income_by_name(self, name: str) -> int:
        """Return an income id that has the given name.

        Args:
            db: database session.
            income_name: the income name.

        Returns:
            income_id: if the income exist.
            None: if the income don't exist.
        """
        income = self.session.scalars(select(Income).where(Income.name == name)).first()
        if not income:
            return None
        return income.id

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
    ) -> int:
        """Create a new income, for a given account and return the new income id.

        Args:
            db: database session.
            account_id: the account id for the income.
            name: name of the income.
            expected_income_value: expected value of the income in cents, it's zero by default.
            real_income_value: real value of the income in cents, it's zero by default.
            income_day: the day of the month of the first income, it's 1 by default.
            income_month: the month of the income, from an enum.
            recurrence: recurrence of the income, from an enum, it's ONE by default.

        Returns:
            account_id: if a new account was created.
            None: if the user_id is not valid or if the account name already exists.
        """

        # Check if the account_id is valid
        account = self.read_account_by_id(account_id=account_id)
        if not account:
            return None

        # Check if the income name already exist
        income = self.read_income_by_name(name=name)
        if income:
            return None

        # Add income to the database
        db_income = Income(
            user_id=user_id,
            account_id=account_id,
            name=name,
            expected_income_value=expected_income_value,
            real_income_value=real_income_value,
            income_day=income_day,
            income_month=income_month,
            recurrence=recurrence,
        )
        self.session.add(db_income)
        self.session.commit()
        self.session.refresh(db_income)
        return db_income.id

    def delete_income(self, income_id: int) -> bool:
        """Delete an income in the database.

        Args:
            db: database session.
            income_id: id of the income to delete.

        Returns:
            True: if deleted.
            False: if not deleted.
        """

        # Check if income exist
        income = self.session.scalars(select(Income).where(Income.id == income_id)).first()
        if not income:
            return False

        # Delete the income
        self.session.delete(income)
        self.session.commit()
        return True

    def read_subcategory_by_name(self, name: str) -> int:
        """Return a subcategory id that has the given subcategory name.

        Args:
            db: database session.
            name: the subcategory name.

        Returns:
            subcategory_id: if the subcategory exist.
            None: if the subcategory don't exist.
        """
        subcategory = self.session.scalars(select(SubCategory).where(SubCategory.name == name)).first()
        if not subcategory:
            return None
        return subcategory.id

    def read_subcategory_list_by_category_id(self, category_id: int) -> list:
        """Return a list of all subcategories from a given category id.

        Args:
            db: database session.
            category_id: category id from where we get the subcategories list

        Returns:
            subcategory_list: list of all subcategories for a given category id, if there is at least one subcategory.
            None: if there is no subcategory, or category_id.
        """

        # Check if the category_id exists
        category = self.read_category_by_id(category_id=category_id)
        if not category:
            return None

        subcategory_list = self.session.scalars(select(SubCategory).where(SubCategory.category_id == category_id)).all()
        if len(subcategory_list) == 0:
            return None
        return subcategory_list

    def add_subcategory(
        self,
        category_id: int,
        name: str,
        recurrent: bool = False,
        recurrence: RecurrenceEnum = "ONE",
        include: bool = True,
    ) -> int:
        """Create a new subcategory in the database, and return the subcategory id.

        Args:
            db: database session.
            name: name of the new subcategory.

        Returns:
            subcategory_id: if a new subcategory was created
            None: if the subcategory failed to be created.
        """
        # Check if name already exist
        subcategory = self.read_subcategory_by_name(name=name)
        if subcategory:
            return None

        # Check if category_id exist
        category = self.read_category_by_id(category_id=category_id)
        if not category:
            return None

        # Check if boolean
        if not isinstance(recurrent, bool) or not isinstance(include, bool):
            return None

        # Check if recurrence is valid
        if recurrence not in RecurrenceEnum.__members__:
            return None

        # Add subcategory to the database
        db_subcategory = SubCategory(
            category_id=category_id,
            name=name,
            recurrent=recurrent,
            recurrence=recurrence,
            include=include,
        )
        self.session.add(db_subcategory)
        self.session.commit()
        self.session.refresh(db_subcategory)
        return db_subcategory.id

    def read_transaction_by_id(self, transaction_id: int) -> Transaction | None:
        """Return a transaction object that has the given id.

        Args:
            db: database session.
            transaction_id: the transaction id.

        Returns:
            transaction: a transaction object if the transaction exist.
            None: if the transaction don't exist.
        """
        transaction = self.session.scalars(select(Transaction).where(Transaction.id == transaction_id)).first()
        if not transaction:
            return None
        return transaction

    def add_transaction(
        self,
        account_id: int,
        subcategory_id: int,
        date: datetime,
        value: int,
        description: str = "",
    ) -> int | None:
        """Create a new transaction in the database, and return the transaction id.

        Args:
            db: database session.
            account_id: the id of the account where the transaction will be created.
            subcategory_id: the id of the category of the transation.
            date: date of the transaction, in datetime format.
            value: value of the transaction in cents, positive if credit, negative if debit.
            description: short description of the transaction.

        Returns:
            trasaction id: if a new transaction was created
            None: if the transaction failed to be created.
        """

        # Check if the account id is valid
        account = self.read_account_by_id(account_id=account_id)
        if not account:
            return None

        # Check if the subcategory id is valid
        #
        #

        # Add account to the database
        db_transaction = Transaction(
            account_id=account_id,
            subcategory_id=subcategory_id,
            date=date,
            value=value,
            description=description,
        )
        self.session.add(db_transaction)
        self.session.commit()
        self.session.refresh(db_transaction)
        return db_transaction.id

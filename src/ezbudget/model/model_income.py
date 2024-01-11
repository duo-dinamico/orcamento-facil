from datetime import date

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from ezbudget.model import Income, RecurrenceEnum


class ModelIncome:
    def __init__(self, parent_model):
        self.parent = parent_model

    def create_income(
        self,
        user_id: int,
        account_id: int,
        name: str,
        expected_income_value: int = 0,
        income_date: date = date.today(),
        currency: str = "EUR",
        recurrence: RecurrenceEnum = RecurrenceEnum.ONE,
    ) -> Income:
        """Create a new income, for a given account and return the new income.

        Args:
            account_id: the account id for the income.
            name: name of the income.
            expected_income_value: expected value of the income in cents, it's zero by default.
            income_date: the expected date of the income. We will only care about day and month.
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
                income_date=income_date,
                currency=currency,
                recurrence=recurrence,
            )
            self.parent.session.add(income)
            self.parent.session.commit()
            self.parent.session.refresh(income)
            return income
        except IntegrityError as e:
            self.parent.session.rollback()
            if "foreign key constraint" in str(e.orig).lower():
                return "User ID or Account ID does not exist"
            elif "unique constraint" in str(e.orig).lower():
                return "Income name already exists"
            else:
                return "An unknown IntegrityError occurred"
        except LookupError as lookup_error:
            self.parent.session.rollback()
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
            return self.parent.read_first_basequery(select(Income).where(Income.name == name))
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
            return self.parent.read_all_basequery(select(Income).where(Income.user_id == user_id))
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
            return self.parent.read_all_basequery(select(Income).where(Income.account_id == account_id))
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
        deleted_row = self.parent.session.query(Income).where(Income.id == id).delete()
        self.parent.session.commit()
        return deleted_row

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound

from ezbudget.model import Transaction, TransactionTypeEnum


class ModelTransaction:
    def __init__(self, parent_model):
        self.parent = parent_model

    def create_transaction(
        self,
        account_id: int,
        subcategory_id: int,
        date: datetime,
        transaction_type: TransactionTypeEnum,
        value: int,
        currency_id: int,
        description: str = None,
        target_account_id: int = None,
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
                transaction_type=transaction_type,
                value=value,
                currency_id=currency_id,
                description=description,
                target_account_id=target_account_id,
            )

            self.parent.session.add(new_transaction)
            self.parent.session.commit()
            self.parent.session.refresh(new_transaction)
            return new_transaction
        except IntegrityError as e:
            self.parent.session.rollback()
            if "foreign key constraint" in str(e.orig).lower():
                return "Either Account ID or SubCategory ID does not exist"
            else:
                return "An unknown IntegrityError occurred"
        except LookupError as lookup_error:
            self.parent.session.rollback()
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
            return self.parent.read_first_basequery(select(Transaction).where(Transaction.id == transaction_id))
        except NoResultFound:
            return None

    def read_transaction_list_by_user(self, user_id: int) -> list:
        """Return a list of all transaction objects of a given user.

        Args:
            user_id: the user id.
        """
        try:
            return self.parent.read_all_basequery(
                select(Transaction)
                .options(joinedload(Transaction.account))
                .where(Transaction.account.has(user_id=user_id))
            )
        except NoResultFound:
            return None

    def read_transaction_list_by_account(self, account_id: int) -> list:
        """Return a list of transactions objects that has the given account_id.

        Args:
            account_id: the account id.

        Returns:
            transaction_list: a list of transactions object if the account exist.
            []: empty list if no transaction with that account.
        """
        try:
            return self.parent.read_all_basequery(select(Transaction).where(Transaction.account_id == account_id))
        except NoResultFound:
            return None

    def read_transaction_list_by_subcategory(self, subcategory_id: int) -> list:
        """Return a list of all transaction objects of a given subcategory.

        Args:
            subcategory_id: the subcategory id.
        """
        try:
            return self.parent.read_all_basequery(
                select(Transaction).where(Transaction.subcategory_id == subcategory_id)
            )
        except NoResultFound:
            return None

    def update_transaction(self, transaction: Transaction) -> None:
        """Update a transaction in the database, and return the transaction.

        Args:
            transaction: the transaction to be updated

        Returns:
            transaction: if the transaction was updated
            None: if the transaction failed to be updated.
        """
        try:
            self.parent.session.add(transaction)
            self.parent.session.commit()
            self.parent.session.refresh(transaction)
            return transaction
        except IntegrityError as e:
            self.parent.session.rollback()
            if "foreign key constraint" in str(e.orig).lower():
                return "Either Account ID or SubCategory ID does not exist"
            else:
                return "An unknown IntegrityError occurred"
        except LookupError as lookup_error:
            self.parent.session.rollback()
            return f"A LookupError occurred: {lookup_error}"

    def delete_transaction(self, transaction_id: int) -> int:
        """Delete a transaction with the given id.

        Args:
            transaction_id: the transaction id.

        Returns:
            Number of rows deleted. Should allways be 1.
        """
        try:
            result = self.parent.session.query(Transaction).where(Transaction.id == transaction_id).delete()
            self.parent.session.commit()
            return result
        except NoResultFound:
            return None

from __future__ import annotations

from calendar import isleap, monthcalendar, monthrange
from datetime import datetime
from typing import Protocol

from ezbudget.model import (
    CategoryTypeEnum,
    CurrencyEnum,
    RecurrenceEnum,
    TransactionTypeEnum,
)
from ezbudget.utils import get_hashed_password, verify_password


class ModelProtocol(Protocol):
    ...


class ViewProtocol(Protocol):
    ...


class Presenter:
    def __init__(self, model: ModelProtocol, view: ViewProtocol) -> None:
        self.model = model
        self.view = view

        self.model_account = model.model_account
        self.model_category = model.model_category
        self.model_income = model.model_income
        self.model_subcategory = model.model_subcategory
        self.model_transaction = model.model_transaction
        self.model_user_subcategory = model.model_user_subcategory
        self.model_user = model.model_user

    # user login and register
    def register(self, user_data) -> None:
        hashed_password = get_hashed_password(user_data["password"])

        response = self.model_user.create_user(username=user_data["username"], password=hashed_password)
        if isinstance(response, str):  # check no error was returned (like existing user)
            self.view.login_view.set_error(response)
            print(response)  # TODO replace this with the log
        else:
            self.model.user = response
            self.view.show_homepage(response)

    def login(self, user_data) -> None:
        response = self.model_user.read_user_by_name(user_data["username"])

        if response is None:  # check user is not None
            self.view.login_view.set_error("Incorrect username and / or password")
        else:
            check_password = verify_password(user_data["password"], response.password)
            if isinstance(check_password, str):
                self.view.login_view.set_error(check_password)
            else:
                self.model.user = response
                self.view.show_homepage(response)

    # account related
    def create_account(self, account_data, account_type):
        check_account_exists = self.model_account.read_account_by_name(name=account_data["name"])

        if account_type == "BANK":
            error_name = "Account"
            method_to_call = self.view.homepage_view.incoming_outgoing.set_account_error
        else:
            error_name = "Credit card"
            method_to_call = self.view.homepage_view.incoming_outgoing.set_credit_card_error

        if check_account_exists:
            method_to_call(f"{error_name} already exists")
        else:
            account_data["user_id"] = self.model.user.id
            account_data["account_type"] = account_type
            response = self.model_account.create_account(**account_data)

            if isinstance(response, str):
                method_to_call(response)
            else:
                self.view.homepage_view.incoming_outgoing.set_account_model()
                self.view.homepage_view.incoming_outgoing.set_credit_card_model()
                self.view.homepage_view.incoming_outgoing.clear_account_data()
                self.view.homepage_view.incoming_outgoing.clear_credit_card_data()
                self.view.homepage_view.transactions.populate_accounts()

    def get_account_list(self, account_type) -> None:
        return self.model_account.read_accounts_by_user(user_id=self.model.user.id, account_type=account_type)

    def get_account_list_by_user(self):
        # Get user account object list
        accounts_list = self.model_account.read_accounts_by_user(user_id=1, account_type="BANK")

        # Transform in a list of names of accounts
        return_list = [account.name for account in accounts_list]

        return return_list

    def get_account_id_by_name(self, account_name):
        return self.model_account.read_account_by_name(name=account_name).id

    def handle_set_total_accounts(self):
        if self.model.user is not None:
            user_accounts = (
                self.model_account.read_accounts_by_user(user_id=self.model.user.id, account_type="BANK") or []
            )
            if len(user_accounts) > 0:
                balance = 0
                for account in user_accounts:
                    balance += account.balance
                return {"balance": balance, "user_accounts": user_accounts}
            return {"balance": 0, "user_accounts": []}

    def get_accounts(self):
        return [account.name for account in self.model_account.read_accounts_by_user(user_id=self.model.user.id)]

    def handle_set_total_credit_cards(self):
        if self.model.user is not None:
            user_cards = self.model_account.read_accounts_by_user(user_id=self.model.user.id, account_type="CARD") or []
            if len(user_cards) > 0:
                balance = 0
                for card in user_cards:
                    balance += card.balance
                return {"balance": balance, "user_cards": user_cards}
            return {"balance": 0, "user_cards": []}

    # incoming related
    def create_income(self, income_data):
        check_income_exists = self.model_income.read_income_by_name(name=income_data["name"])

        if check_income_exists:
            self.view.homepage_view.incoming_outgoing.set_income_error("Income source name already exists")
        else:
            account = self.model_account.read_account_by_name(name=income_data["account_name"])
            income_data["account_id"] = account.id
            del income_data["account_name"]
            income_data["user_id"] = self.model.user.id
            income_data["income_date"] = datetime.strptime(income_data["income_date"], "%Y/%m/%d").date()
            for recurrence in RecurrenceEnum:
                if recurrence.value == income_data["recurrence"]:
                    income_data["recurrence"] = recurrence.name
            response = self.model_income.create_income(**income_data)

            if isinstance(response, str):
                self.view.homepage_view.incoming_outgoing.set_income_error(response)
            else:
                self.view.homepage_view.incoming_outgoing.set_incoming_model()
                self.view.homepage_view.incoming_outgoing.clear_income_data()
                self.view.homepage_view.monthly_budget.set_table_selection()

    def get_income_list(self) -> None:
        return self.model_income.read_incomes_by_user(user_id=self.model.user.id)

    # categories related
    def create_category(self, category_data):
        for category_type in CategoryTypeEnum:
            if category_type.value == category_data["category_type"]:
                category_data["category_type"] = category_type.name
        self.model_category.create_category(**category_data)
        self.view.homepage_view.manage_categories.set_categories_and_subcategories()

    def create_subcategory(self, subcategory_data):
        category_id = self.model_category.read_category_by_name(subcategory_data["category_name"]).id
        subcategory_data["category_id"] = category_id
        del subcategory_data["category_name"]
        for recurrence in RecurrenceEnum:
            if recurrence.value == subcategory_data["recurrence"]:
                subcategory_data["recurrence"] = recurrence.name
        self.model_subcategory.create_subcategory(**subcategory_data)
        self.view.homepage_view.manage_categories.set_categories_and_subcategories()

    def get_category_list(self) -> None:
        return self.model_category.read_categories()

    def get_subcategory_list(self) -> None:
        return self.model_subcategory.read_subcategories()

    def get_subcategory_id_by_name_and_category(self, subcategory_name, category_id):
        return self.model_subcategory.read_subcategory_by_name(name=subcategory_name, category_id=category_id).id

    def get_category_id_by_name(self, category_name):
        return self.model_category.read_category_by_name(category_name).id

    def add_user_category(self, subcategory_id) -> None:
        check_user_subcategory_exists = self.model_user_subcategory.read_user_subcategories_multiple_args(
            user_id=self.model.user.id, subcategory_id=subcategory_id
        )
        if check_user_subcategory_exists is None:
            self.model_user_subcategory.create_user_subcategory(
                user_id=self.model.user.id, subcategory_id=subcategory_id
            )
            self.view.homepage_view.transactions.populate_subcategories()
            self.view.homepage_view.monthly_budget.total_budgeted()
            self.view.homepage_view.monthly_budget.set_table_selection()

    def remove_user_category(self, subcategory_id: int):
        removed_user_category = self.model_user_subcategory.delete_user_subcategory(subcategory_id=subcategory_id)
        self.view.homepage_view.transactions.populate_subcategories()
        self.view.homepage_view.monthly_budget.set_table_selection()
        return removed_user_category

    def get_user_subcategory_list(self):
        # Get user subcategory object list
        user_subcategory_list = self.model_user_subcategory.read_user_subcategories_by_user(user_id=self.model.user.id)

        # Transform in a list of names of subcategories
        return_list = [
            [
                f"{user_subcategory.subcategory.category.name} - {user_subcategory.subcategory.name}",
                f"{user_subcategory.subcategory.currency.value if user_subcategory.subcategory.currency is not None else None} {user_subcategory.subcategory.recurrence_value}",
            ]
            for user_subcategory in user_subcategory_list
        ]
        return return_list

    def get_total_budgeted(self):
        user_subcategory_list = self.model_user_subcategory.read_user_subcategories_by_user(user_id=self.model.user.id)
        income_sources_list = self.model_income.read_incomes_by_user(user_id=self.model.user.id)
        budgeted_income = 0
        budgeted_expenses = 0
        current_year = datetime.now().year
        current_month = datetime.now().month
        number_of_weeks = len(monthcalendar(current_year, current_month))
        number_of_days = monthrange(current_year, current_month)[1]
        for expense in user_subcategory_list:
            if expense.subcategory.recurrent:
                budgeted_expenses += self.monthly_recurrence_balance(
                    expense.subcategory, number_of_days, number_of_weeks
                )
        for income in income_sources_list:
            if income.recurrent:
                budgeted_income += self.monthly_recurrence_balance(income, number_of_days, number_of_weeks)

        return {"budgeted_income": budgeted_income, "budgeted_expenses": budgeted_expenses}

    def get_total_real(self):
        transaction_list = self.model_transaction.read_transaction_list_by_user(user_id=self.model.user.id)
        total_income = 0
        total_expenses = 0
        current_year = datetime.now().year
        current_month = datetime.now().month
        for x in transaction_list:
            transaction_date: datetime = x.date
            if transaction_date.year == current_year and transaction_date.month == current_month:
                if x.transaction_type == TransactionTypeEnum.Income:
                    total_income += x.value
                if x.transaction_type == TransactionTypeEnum.Expense:
                    total_expenses += x.value

        return {"total_income": total_income, "total_expenses": total_expenses}

    # transaction related
    def create_transaction(self, transaction_data) -> None:
        """Create a transaction in Model, when activated in View."""
        updated_transaction = self.format_transaction_data(transaction_data)

        # Create the transaction in the model
        transaction = self.model_transaction.create_transaction(**updated_transaction)

        if transaction:
            account = self.model_account.read_account_by_id(transaction.account_id)
            if transaction.transaction_type == TransactionTypeEnum.Income:
                account.balance += transaction.value
            elif transaction.transaction_type == TransactionTypeEnum.Expense:
                account.balance -= transaction.value
            elif transaction.transaction_type == TransactionTypeEnum.Transfer:
                transfer_account = self.model_account.read_account_by_id(transaction.target_account_id)
                account.balance -= transaction.value
                transfer_account.balance += transaction.value
                self.model_account.update_account(transfer_account)
            self.model_account.update_account(account)
            self.view.homepage_view.transactions.set_transactions_model()
            self.view.homepage_view.transactions.clear_fields()
            self.view.homepage_view.incoming_outgoing.set_account_model()
            self.view.homepage_view.incoming_outgoing.set_credit_card_model()
            self.view.homepage_view.monthly_budget.set_table_selection()

    def update_transaction(
        self,
        transaction_id: int,
        transaction_data: dict,
        previous_value: int,
        previous_account_id: int,
        previous_transaction_type: TransactionTypeEnum,
    ) -> None:
        """Presenter method that call model to update transaction."""

        # update the transaction from the model with the new values
        transaction_to_update = self.model_transaction.read_transaction_by_id(transaction_id)
        formatted_transaction_data = self.format_transaction_data(transaction_data)

        # we update the values on the transaction to update with the transaction data value
        for key, value in formatted_transaction_data.items():
            setattr(transaction_to_update, key, value)

        # update the value in the accounts
        previous_account = self.model_account.read_account_by_id(previous_account_id)
        new_account = self.model_account.read_account_by_id(formatted_transaction_data["account_id"])

        if previous_account.name != new_account.name:
            if transaction_to_update.transaction_type != previous_transaction_type.name:
                if transaction_to_update.transaction_type == "Income":
                    previous_account.balance += previous_value
                    new_account.balance += transaction_to_update.value
                else:
                    previous_account.balance -= previous_value
                    new_account.balance -= transaction_to_update.value
            else:
                if transaction_to_update.transaction_type == "Income":
                    previous_account.balance -= transaction_to_update.value
                    new_account.balance += transaction_to_update.value
                else:
                    previous_account.balance += transaction_to_update.value
                    new_account.balance -= transaction_to_update.value
        else:
            difference = transaction_to_update.value - previous_value
            if transaction_to_update.transaction_type != previous_transaction_type.name:
                if transaction_to_update.transaction_type == "Income":
                    previous_account.balance += previous_value
                    previous_account.balance += transaction_to_update.value
                if transaction_to_update.transaction_type == "Expense":
                    previous_account.balance -= previous_value
                    previous_account.balance -= transaction_to_update.value
            else:
                if transaction_to_update.transaction_type == "Transfer":
                    target_account = self.model_account.read_account_by_id(
                        formatted_transaction_data["target_account_id"]
                    )
                    target_account.balance = (
                        target_account.balance - abs(difference)
                        if difference < 0
                        else target_account.balance + abs(difference)
                    )
                    self.model_account.update_account(target_account)
                previous_account.balance = (
                    previous_account.balance + abs(difference)
                    if difference < 0
                    else previous_account.balance - abs(difference)
                )

        self.model_account.update_account(previous_account)
        self.model_account.update_account(new_account)

        # Send data to model process
        self.model_transaction.update_transaction(transaction_to_update)

        # update views and their models
        self.view.homepage_view.transactions.set_transactions_model()
        self.view.homepage_view.transactions.clear_fields()
        self.view.homepage_view.incoming_outgoing.set_account_model()
        self.view.homepage_view.incoming_outgoing.set_credit_card_model()
        self.view.homepage_view.monthly_budget.set_table_selection()

    def get_transactions_list(self) -> None:
        # TODO Account type
        return self.model_transaction.read_transaction_list_by_user(user_id=self.model.user.id)

    def remove_transaction(
        self, transaction_data, transaction_id: int, account_id: int, target_account_id: int
    ) -> None:
        """Presenter method that call model to delete transaction."""
        account = self.model_account.read_account_by_id(account_id)
        transaction_value = int(transaction_data["value"])
        if transaction_data["transaction_type"] == "Income":
            account.balance -= transaction_value
        elif transaction_data["transaction_type"] == "Expense":
            account.balance += transaction_value
        elif transaction_data["transaction_type"] == "Transfer":
            target_account = self.model_account.read_account_by_id(target_account_id)
            account.balance += transaction_value
            target_account.balance -= transaction_value
            self.model_account.update_account(target_account)

        self.model_account.update_account(account)

        # Delete
        self.model_transaction.delete_transaction(transaction_id)

        # Refresh view
        self.view.homepage_view.transactions.set_transactions_model()
        self.view.homepage_view.transactions.clear_fields()
        self.view.homepage_view.incoming_outgoing.set_account_model()
        self.view.homepage_view.incoming_outgoing.set_credit_card_model()
        self.view.homepage_view.monthly_budget.set_table_selection()

    def get_month_summary(self):
        user_categories_list = self.model_user_subcategory.read_user_subcategories_by_user(user_id=self.model.user.id)
        month_summary = []
        current_year = datetime.now().year
        current_month = datetime.now().month
        number_of_weeks = len(monthcalendar(current_year, current_month))
        number_of_days = monthrange(current_year, current_month)[1]
        for x in user_categories_list:
            transaction_summary = []
            if x.subcategory.recurrent:
                category_subcategory_name = f"{x.subcategory.category.name} - {x.subcategory.name}"
                transaction_summary.append(category_subcategory_name)
                anual_budget = self.yearly_recurrence_balance(x.subcategory) / 100
                transaction_summary.append(anual_budget)
                recurrent_value = self.monthly_recurrence_balance(x.subcategory, number_of_days, number_of_weeks) / 100
                transaction_summary.append(recurrent_value)
                transaction_summary.append(x.subcategory.recurrence.value)
                subcategory_transactions = self.model_transaction.read_transaction_list_by_subcategory(
                    subcategory_id=x.subcategory_id
                )
                current_month_transactions_value = 0
                for y in subcategory_transactions:
                    transaction_date: datetime = y.date
                    if transaction_date.year == current_year and transaction_date.month == current_month:
                        current_month_transactions_value += y.value / 100
                transaction_summary.append(current_month_transactions_value)
                transaction_summary.append(recurrent_value - current_month_transactions_value)

                month_summary.append(transaction_summary)
        return month_summary

    # utils
    def get_currency(self):
        return CurrencyEnum

    def get_transaction_types(self):
        return TransactionTypeEnum

    def get_recurrence(self):
        return RecurrenceEnum

    def get_category_type(self):
        return [category_type.value for category_type in CategoryTypeEnum]

    def format_transaction_data(self, transaction_data):
        keys_to_remove = ["account_name", "subcategory_name", "target_account_name"]
        formatted_transaction_data = {**transaction_data}

        # get account id using account name
        account_id = self.model_account.read_account_by_name(transaction_data["account_name"]).id
        formatted_transaction_data["account_id"] = account_id

        # get targret account id using account name
        if transaction_data["target_account_name"]:
            target_account_id = self.model_account.read_account_by_name(transaction_data["target_account_name"]).id
            formatted_transaction_data["target_account_id"] = target_account_id

        # split the user subcategory to get category and subcatebory id
        subcategory_split = transaction_data["subcategory_name"].split(" - ")
        category_id = self.get_category_id_by_name(subcategory_split[0])
        subcategory_id = self.model_subcategory.read_subcategory_by_name(subcategory_split[1], category_id).id
        formatted_transaction_data["subcategory_id"] = subcategory_id

        # update date string to string format
        formatted_transaction_data["date"] = datetime.strptime(transaction_data["date"], "%Y/%m/%d").date()

        # update the transaction value to int
        formatted_transaction_data["value"] = int(transaction_data["value"])

        # remove unecessary fields
        for key in keys_to_remove:
            del formatted_transaction_data[key]

        return formatted_transaction_data

    def monthly_recurrence_balance(self, recurrence, number_of_days: int, number_of_weeks: int) -> int:
        monthly_balance = 0
        if recurrence.recurrence == RecurrenceEnum.DAY:
            monthly_balance += recurrence.recurrence_value * number_of_days
        if recurrence.recurrence == RecurrenceEnum.WEEK:
            monthly_balance += recurrence.recurrence_value * number_of_weeks
        if recurrence.recurrence == RecurrenceEnum.MONTH:
            monthly_balance += recurrence.recurrence_value
        if recurrence.recurrence == RecurrenceEnum.YEAR:
            monthly_balance += recurrence.recurrence_value / 12
        return monthly_balance

    def yearly_recurrence_balance(self, recurrence) -> int:
        yearly_balance = 0
        current_year = datetime.now().year
        number_of_days = 366 if isleap(current_year) else 365
        number_of_weeks = 52
        number_of_months = 12
        if recurrence.recurrence == RecurrenceEnum.DAY:
            yearly_balance += recurrence.recurrence_value * number_of_days
        if recurrence.recurrence == RecurrenceEnum.WEEK:
            yearly_balance += recurrence.recurrence_value * number_of_weeks
        if recurrence.recurrence == RecurrenceEnum.MONTH:
            yearly_balance += recurrence.recurrence_value * number_of_months
        if recurrence.recurrence == RecurrenceEnum.YEAR:
            yearly_balance += recurrence.recurrence_value

        return yearly_balance

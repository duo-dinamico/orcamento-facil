from __future__ import annotations

from datetime import datetime
from typing import Protocol

from ezbudget.model import CategoryTypeEnum, CurrencyEnum, RecurrenceEnum
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
                self.view.homepage_view.transactions.populate_target_accounts()

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

    def get_target_accounts(self):
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

    def remove_user_category(self, subcategory_id: int):
        removed_user_category = self.model_user_subcategory.delete_user_subcategory(subcategory_id=subcategory_id)
        self.view.homepage_view.transactions.populate_subcategories()
        return removed_user_category

    def get_user_subcategory_list(self):
        # Get user subcategory object list
        user_subcategory_list = self.model_user_subcategory.read_user_subcategories_by_user(user_id=self.model.user.id)

        # Transform in a list of names of subcategories
        return_list = [
            f"{user_subcategory.subcategory.category.name} - {user_subcategory.subcategory.name}"
            for user_subcategory in user_subcategory_list
        ]
        return return_list

    # transaction related
    def create_transaction(self, transaction_data) -> None:
        """Create a transaction in Model, when activated in View."""
        updated_transaction = self.update_transaction_dict(transaction_data)

        # Create the transaction in the model
        transaction = self.model_transaction.create_transaction(**updated_transaction)

        if transaction:
            account = self.model_account.read_account_by_id(transaction.account_id)
            if transaction.value >= 0:
                account.balance += transaction.value
            else:
                account.balance -= abs(transaction.value)
            self.model_account.update_account(account)
            self.view.homepage_view.transactions.set_transactions_model()
            self.view.homepage_view.incoming_outgoing.set_account_model()
            self.view.homepage_view.incoming_outgoing.set_credit_card_model()

    def update_transaction(self, transaction_id: int, transaction_data, previous_value, previous_account_id) -> None:
        """ " Presenter method that call model to update transaction."""

        # update the transaction from the model with the new values
        transaction = self.model_transaction.read_transaction_by_id(transaction_id)
        updated_transaction = self.update_transaction_dict(transaction_data)
        for key, value in updated_transaction.items():
            setattr(transaction, key, value)

        # convert to int
        transaction.value = int(transaction.value)
        int_previous_value = int(previous_value)

        # update the value in the accounts
        previous_account = self.model_account.read_account_by_id(previous_account_id)
        new_account = self.model_account.read_account_by_id(updated_transaction["account_id"])

        direction = -1 if int_previous_value > transaction.value else 1
        difference = abs(int_previous_value - transaction.value)
        if previous_account.name != new_account.name:
            if int_previous_value != transaction.value:
                if int_previous_value > 0:
                    previous_account.balance -= abs(int_previous_value)
                else:
                    previous_account.balance += abs(int_previous_value)
                if transaction.value > 0:
                    new_account.balance += abs(transaction.value)
                else:
                    new_account.balance -= abs(transaction.value)
            else:
                if transaction.value > 0:
                    previous_account.balance -= transaction.value
                    new_account.balance += transaction.value
                else:
                    previous_account.balance += abs(transaction.value)
                    new_account.balance -= abs(transaction.value)

            self.model_account.update_account(previous_account)
            self.model_account.update_account(new_account)

        elif previous_account.name == new_account.name and int_previous_value != transaction.value:
            previous_account.balance += difference * direction
            self.model_account.update_account(previous_account)

        # Send data to model process
        self.model_transaction.update_transaction(transaction)

        # update models and tables
        self.view.homepage_view.transactions.set_transactions_model()
        self.view.homepage_view.incoming_outgoing.set_account_model()
        self.view.homepage_view.incoming_outgoing.set_credit_card_model()

    def get_transactions_list(self) -> None:
        # TODO Account type
        return self.model_transaction.read_transaction_list_by_user(user_id=self.model.user.id)

    def remove_transaction(self, transaction_data, transaction_id) -> None:
        """Presenter method that call model to delete transaction."""
        account_id = self.model_account.read_account_by_name(transaction_data["account_name"]).id
        account = self.model_account.read_account_by_id(account_id)
        transaction_value = int(transaction_data["value"])
        if transaction_value >= 0:
            account.balance -= transaction_value
        else:
            account.balance += abs(transaction_value)
        self.model_account.update_account(account)

        # Delete
        self.model_transaction.delete_transaction(transaction_id)

        # Refresh view
        self.view.homepage_view.transactions.set_transactions_model()
        self.view.homepage_view.incoming_outgoing.set_account_model()
        self.view.homepage_view.incoming_outgoing.set_credit_card_model()

    # utils
    def get_currency(self):
        return CurrencyEnum

    def get_recurrence(self):
        return RecurrenceEnum

    def get_category_type(self):
        return [category_type.value for category_type in CategoryTypeEnum]

    def update_transaction_dict(self, transaction_data):
        account_id = self.model_account.read_account_by_name(transaction_data["account_name"]).id
        transaction_data["account_id"] = account_id
        del transaction_data["account_name"]
        subcategory_split = transaction_data["subcategory_name"].split(" - ")
        category_id = self.get_category_id_by_name(subcategory_split[0])
        subcategory_id = self.model_subcategory.read_subcategory_by_name(subcategory_split[1], category_id).id
        transaction_data["subcategory_id"] = subcategory_id
        del transaction_data["subcategory_name"]
        transaction_data["date"] = datetime.strptime(transaction_data["date"], "%Y/%m/%d").date()

        return transaction_data

from __future__ import annotations

from typing import Protocol

from ezbudget.model import CurrencyEnum, MonthEnum, RecurrenceEnum
from ezbudget.utils import get_hashed_password, verify_password


class ModelProtocol(Protocol):
    def create_user(self, username, password):
        ...

    def read_user_by_name(self, username):
        ...

    def create_account(self, name, user_id, account_type, balance, currency):
        ...

    def create_income(
        self, user_id, account_id, name, expected_income_value, real_income_value, income_day, income_month, recurrence
    ):
        ...

    def read_account_by_name(self, name):
        ...

    def read_accounts_by_user(self, user_id, account_type):
        ...

    def read_account_by_id(self, id):
        ...

    def read_income_by_name(self, name):
        ...

    def read_incomes_by_user(self, user_id):
        ...

    def read_categories(self):
        ...

    def read_subcategories(self):
        ...

    def create_user_subcategory(self):
        ...

    def read_user_subcategories_multiple_args(self, user_id, subcategory_id):
        ...

    def read_user_subcategories_by_user(self, user_id):
        ...

    def delete_user_subcategory(self, id):
        ...


class ViewProtocol(Protocol):
    def init_ui(self, presenter):
        ...

    def error_message_set(self, target, message):
        ...

    def show_register_login(self, presenter):
        ...

    def show_incomig_outgoing(self, event):
        ...

    def get_user_data(self):
        ...

    def get_account_data(self):
        ...

    def get_income_data(self):
        ...

    def get_credit_card_data(self):
        ...

    def show_create_account_popup(self, event):
        ...

    def destroy_current_popup(self):
        ...

    def account_selected(self, event):
        ...

    def show_homepage(self, event):
        ...


class Presenter:
    def __init__(self, model: ModelProtocol, view: ViewProtocol) -> None:
        self.model = model
        self.view = view

    def handle_register_user(self, event=None) -> None:
        del event  # not used in this function
        user_data = self.view.get_user_data()
        check_user_exists = self.model.read_user_by_name(user_data["username"])

        if check_user_exists:
            self.view.error_message_set("frame", "User already exists")
        else:
            hashed_password = get_hashed_password(user_data["password"])
            try:
                user = self.model.create_user(username=user_data["username"], password=hashed_password)
                self.model.user = user
                self.view.show_incomig_outgoing()
            except Exception as error:  # pylint: disable=broad-exception-caught
                self.view.error_message_set("frame", "Was not able to create user")
                # TODO replace this with the log
                print(error)

    def handle_add_user_category(self, subcategory_id) -> None:
        check_user_subcategory_exists = self.model.read_user_subcategories_multiple_args(
            user_id=self.model.user.id, subcategory_id=subcategory_id
        )
        if check_user_subcategory_exists is None:
            self.model.create_user_subcategory(user_id=self.model.user.id, subcategory_id=subcategory_id)

    def handle_login_user(self, event=None) -> None:
        del event  # not used in this function
        user_data = self.view.get_user_data()
        user = self.model.read_user_by_name(user_data["username"])

        if user:
            check_password = verify_password(user_data["password"], user.password)
            if check_password:
                self.model.user = user
                self.view.show_homepage()
            else:
                self.view.error_message_set("frame", "Wrong username or password")
        else:
            self.view.error_message_set("frame", "User not found")

    def handle_create_account(self, event=None):
        del event  # not used in this function
        account_data = self.view.get_account_data()
        check_account_exists = self.model.read_account_by_name(name=account_data["name"])

        if check_account_exists:
            self.view.error_message_set("top", "Account already exists")
        else:
            account_data["user_id"] = self.model.user.id
            account = self.model.create_account(**account_data)

            if account:
                # * This is necessary for when the pop up is called outside of incoming outgoing view
                if hasattr(self.view.current_frame, "create_account") and callable(
                    self.view.current_frame.create_account
                ):
                    self.view.current_frame.create_account(account)
                if hasattr(self.view.current_frame, "refresh_total_and_accounts") and callable(
                    self.view.current_frame.refresh_total_and_accounts
                ):
                    self.view.current_frame.refresh_total_and_accounts()
                self.view.destroy_current_popup()

    def handle_create_income(self, event=None):
        del event  # not used in this function
        income_data = self.view.get_income_data()
        check_income_exists = self.model.read_income_by_name(name=income_data["name"])

        if check_income_exists:
            self.view.error_message_set("top", "Income source already exists")
        else:
            account = self.model.read_account_by_name(name=income_data["account_name"])
            income_data["account_id"] = account.id
            del income_data["account_name"]
            income_data["user_id"] = self.model.user.id
            for recurrence in RecurrenceEnum:
                if recurrence.value == income_data["recurrence"]:
                    income_data["recurrence"] = recurrence.name
            income = self.model.create_income(**income_data)

        if income:
            self.view.current_frame.create_income(income)
            self.view.destroy_current_popup()

    def handle_create_credit_card(self, event=None):
        del event  # not used in this function
        credit_card_data = self.view.get_credit_card_data()
        check_credit_card_exists = self.model.read_account_by_name(name=credit_card_data["name"])

        if check_credit_card_exists:
            self.view.error_message_set("top", "Credit card already exists")
        else:
            credit_card_data["user_id"] = self.model.user.id
            credit_card = self.model.create_account(**credit_card_data)

        if credit_card:
            self.view.current_frame.add_credit_card(credit_card)
            self.view.destroy_current_popup()

    def handle_create_transaction(self, _) -> None:
        """Create a transaction in Model, when activated in View."""

        # Get values from the View
        transaction_data = self.view.get_transaction_data()

        # Create the transaction in the model
        transaction = self.model.create_transaction(**transaction_data)

        if transaction:
            self.view.destroy_current_popup()
            self.view.current_frame.refresh_transactions()

    def refresh_account_list(self) -> None:
        return self.model.read_accounts_by_user(user_id=self.model.user.id, account_type="BANK")

    def refresh_income_list(self) -> None:
        return self.model.read_incomes_by_user(user_id=self.model.user.id)

    def refresh_credit_card_list(self) -> None:
        return self.model.read_accounts_by_user(user_id=self.model.user.id, account_type="CARD")

    def refresh_transactions_list(self) -> None:
        # TODO Account type
        return self.model.read_transaction_list_by_user(user_id=self.model.user.id)

    def remove_transaction(self, transaction_id):
        """Presenter method that call model to delete transaction."""
        # TODO model DELETE
        print("TRANSACTION ID", transaction_id)

    def refresh_category_list(self) -> None:
        return self.model.read_categories()

    def refresh_subcategory_list(self) -> None:
        return self.model.read_subcategories()

    def refresh_selected_category_list(self) -> None:
        return self.model.read_user_subcategories_by_user(user_id=self.model.user.id)

    def get_currency(self):
        return list(CurrencyEnum.__members__.keys())

    def get_account_list_by_user(self):
        # TODO define a dummy user
        self.model.user = self.model.read_user_by_id(id=1)

        # Get user account object list
        accounts_list = self.model.read_accounts_by_user(user_id=self.model.user.id, account_type="BANK")

        # Transform in a list of names of accounts
        return_list = [account.name for account in accounts_list]

        return return_list

    def get_subcategory_list(self):
        # Get user subcategory object list
        # TODO read_subcategory_list
        subcategory_list = self.model.read_subcategories()

        # Transform in a list of names of subcategories
        return_list = [subcategory.name for subcategory in subcategory_list]
        return return_list

    def get_account_id_by_name(self, account_name):
        return self.model.read_account_by_name(name=account_name).id

    def get_recurrence(self):
        return [recurrence.value for recurrence in RecurrenceEnum]

    def get_target_accounts(self):
        return [
            account.name
            for account in self.model.read_accounts_by_user(user_id=self.model.user.id, account_type="BANK")
        ]

    def handle_remove_user_category(self, subcategory_id: int):
        return self.model.delete_user_subcategory(subcategory_id=subcategory_id)

    def get_month(self):
        return list(MonthEnum.__members__.keys())

    def handle_set_username(self):
        if self.model.user is not None:
            return self.model.user.username
        return "User"

    def handle_set_total_accounts(self):
        if self.model.user is not None:
            user_accounts = self.model.read_accounts_by_user(user_id=self.model.user.id, account_type="BANK")
            if len(user_accounts) > 0:
                balance = 0
                for account in user_accounts:
                    balance += account.balance
                return {"balance": balance, "user_accounts": user_accounts}
            return 0

    def run(self) -> None:
        self.view.init_ui(self)
        self.view.mainloop()

    # TODO Delete this after tests
    def login_dummy_data(self):
        self.model.user = self.model.read_user_by_id(1)
        # self.model.create_category("teste45")
        self.model.create_subcategory(category_id=1, name="str", recurrent=False, recurrence="ONE", include=True)

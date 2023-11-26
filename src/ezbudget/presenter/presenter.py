from __future__ import annotations

from typing import Protocol

from ezbudget.model import CurrencyEnum, MonthEnum, RecurrenceEnum
from ezbudget.utils import get_hashed_password, verify_password


class Model(Protocol):
    def create_user(self, username: str, password: str = ""):
        ...

    def read_user_by_name(self, username: str):
        ...

    def create_account(
        self,
        name: str,
        user_id: int,
        account_type: str,
        initial_balance: int = 0,
        currency: str = "EUR",
    ):
        ...

    def create_income(
        self,
        user_id: int,
        account_id: int,
        name: str,
        expected_income_value: int,
        real_income_value: int,
        income_day: str,
        income_month,
        recurrence,
    ):
        ...

    def read_account_by_name(self, name: str):
        ...

    def read_accounts_by_user(self, user_id: int, account_type: str):
        ...

    def read_account_by_id(self, id: str):
        ...

    def read_income_by_name(self, name: str):
        ...

    def read_incomes_by_user(self, user_id: int):
        ...


class View(Protocol):
    def init_ui(self, presenter: Presenter):
        ...

    def error_message_set(self, target: str, message: str):
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


class Presenter:
    def __init__(self, model: Model, view: View) -> None:
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

    def handle_login_user(self, event=None) -> None:
        del event  # not used in this function
        user_data = self.view.get_user_data()
        user = self.model.read_user_by_name(user_data["username"])

        if user:
            check_password = verify_password(user_data["password"], user.password)
            if check_password:
                self.model.user = user
                # TODO this is supposed to change to the main view
                self.view.show_incomig_outgoing()
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
            self.view.current_frame.create_account(account)
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

    def refresh_account_list(self) -> None:
        return self.model.read_accounts_by_user(user_id=self.model.user.id, account_type="BANK")

    def refresh_income_list(self) -> None:
        return self.model.read_incomes_by_user(user_id=self.model.user.id)

    def refresh_credit_card_list(self) -> None:
        return self.model.read_accounts_by_user(user_id=self.model.user.id, account_type="CARD")

    def refresh_transactions_list(self) -> None:
        # Just a sample list
        return [{"id": 0, "account_id": 1}, {"id": 1, "account_id": 2}]

    def get_currency(self):
        return list(CurrencyEnum.__members__.keys())

    def get_recurrence(self):
        return [recurrence.value for recurrence in RecurrenceEnum]

    def get_target_accounts(self):
        return [
            account.name
            for account in self.model.read_accounts_by_user(user_id=self.model.user.id, account_type="BANK")
        ]

    def get_month(self):
        return list(MonthEnum.__members__.keys())

    def run(self) -> None:
        self.view.init_ui(self)
        self.view.mainloop()
        self.view.init_ui(self)
        self.view.mainloop()

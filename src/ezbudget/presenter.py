from __future__ import annotations

from typing import Protocol

from .model.model import Model
from .utils import get_hashed_password, verify_password


class View(Protocol):
    def init_ui(self, presenter: Presenter) -> None:
        ...

    def error_message_set(self, message: str) -> None:
        ...

    def show_register_login_popup(self, presenter):
        ...

    def show_starting_view(self, event=None):
        ...

    def get_user_data(self) -> {str, str}:
        ...

    def get_account_data(self) -> {str, str}:
        ...

    def show_add_account_popup(self, event=None) -> None:
        ...

    def destroy_current_popup(self) -> None:
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
            self.view.error_message_set("User already exists")
        else:
            hashed_password = get_hashed_password(user_data["password"])
            try:
                user = self.model.add_user(username=user_data["username"], password=hashed_password)
                self.model.user = user
                self.view.show_starting_view()
            except Exception as error:  # pylint: disable=broad-exception-caught
                self.view.error_message_set("Was not able to create user")
                # TODO replace this with the log
                print(error)

    def handle_login_user(self, event=None) -> None:
        del event  # not used in this function
        user_data = self.view.get_user_data()
        user = self.model.read_user_by_name(user_data["username"])

        if user:
            check_password = verify_password(user_data["password"], user.password)
            if check_password:
                # TODO
                self.model.user = user
                self.view.error_message_set(user)
            else:
                self.view.error_message_set("Wrong username or password")
        else:
            self.view.error_message_set("User not found")

    def handle_add_account(self, event=None):
        del event  # not used in this function
        account_data = self.view.get_account_data()
        check_account_exists = self.model.read_account_by_name(account_data["account_name"])

        account = None
        if check_account_exists:
            self.view.error_message_set("Account already exists")
        else:
            try:
                account = self.model.add_account(
                    account_name=account_data["account_name"],
                    user_id=self.model.user.id,
                    initial_balance=account_data["initial_balance"],
                    account_type="BANK",
                    currency=account_data["currency"],
                )
            except Exception as error:  # pylint: disable=broad-exception-caught
                self.view.error_message_set("Was not able to create account")
                # TODO replace this with the log
                print(error)

        if account:
            # TODO refresh account list
            self.refresh_account_list()
            self.view.destroy_current_popup()

    def refresh_account_list(self) -> None:
        accounts_list = self.model.read_accounts_by_user(self.model.user.id)
        print(accounts_list)

    def run(self) -> None:
        self.view.init_ui(self)
        self.view.mainloop()

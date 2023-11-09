from __future__ import annotations
from typing import Protocol

from model import Model
from utils import get_hashed_password, verify_password


class View(Protocol):
    def init_ui(self, presenter: Presenter) -> None:
        ...

    def error_message_set(self, message: str) -> None:
        ...

    def show_register_login_popup(self):
        ...

    def show_starting_view(self, event=None):
        ...

    def get_username_and_password(self) -> {str, str}:
        ...


class Presenter:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view

    def handle_register_user(self, event=None) -> None:
        user_data = self.view.get_username_and_password()
        check_user_exists = self.model.read_user_by_name(user_data["username"])

        if check_user_exists:
            self.view.error_message_set("User already exists")
        else:
            hashed_password = get_hashed_password(user_data["password"])
            try:
                self.model.add_user(username=user_data["username"], password=hashed_password)
                self.view.show_starting_view()
            except:
                self.view.error_message_set("Was not able to create user")

    def handle_login_user(self, event=None) -> None:
        user_data = self.view.get_username_and_password()
        user = self.model.read_user_by_name(user_data["username"])

        if user:
            check_password = verify_password(user_data["password"], user.password)
            if check_password:
                # TODO
                self.view.error_message_set("Move to account summary")
            else:
                self.view.error_message_set("Wrong username or password")
        else:
            self.view.error_message_set("User not found")

    def run(self) -> None:
        self.view.init_ui(self)
        self.view.mainloop()

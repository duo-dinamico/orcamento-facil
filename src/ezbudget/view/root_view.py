import tkinter as tk
from typing import Protocol

from . import add_account_popup_view, register_login_popup_view, starting_view

TITLE = "Ez Budget"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800


class Presenter(Protocol):
    def handle_register_user(self, event=None):
        ...

    def handle_login_user(self, event=None) -> None:
        ...

    def handle_add_account(self, event=None):
        ...

    def run(self) -> None:
        ...


class RootView(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(TITLE)
        self.resizable(False, False)
        self.presenter = None
        self.starting_view = None

        self.current_frame = None
        self.current_popup = None

        # Put the windows in the center of the screen
        x_center = self.winfo_screenwidth() / 2 - WINDOW_WIDTH / 2
        y_center = self.winfo_screenheight() / 2 - WINDOW_HEIGHT / 2
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{int(x_center)}+{int(y_center)}")

    def init_ui(self, presenter: Presenter) -> None:
        self.presenter = presenter
        self.starting_view = starting_view.StartingView(self, presenter)

        self.show_register_login_popup(presenter)

    def error_message_set(self, message: str) -> None:
        self.current_popup.error_message.set(message)

    def get_user_data(self) -> {str, str}:
        return {
            "username": self.current_popup.username_popup.get(),
            "password": self.current_popup.password_popup.get(),
        }

    def get_account_data(self) -> {str, str, str}:
        return {
            "account_name": self.current_popup.account_name.get(),
            "initial_balance": self.current_popup.initial_balance.get(),
            "currency": self.current_popup.currency_combobox.get(),
        }

    def show_register_login_popup(self, presenter) -> None:
        if self.current_popup:
            self.current_popup.destroy()
        self.current_popup = register_login_popup_view.RegisterLogin(self, presenter)

    def show_starting_view(self, event=None) -> None:
        del event  # not used in this function
        if self.current_popup:
            self.current_popup.destroy()
        self.current_frame = self.starting_view
        self.current_frame.pack(expand=True, fill="both")

    def show_add_account_popup(self, event=None) -> None:
        del event  # not used in this function
        if self.current_popup:
            self.current_popup.destroy()
        self.current_popup = add_account_popup_view.AddAccountPopUp(self.current_frame, self.presenter)

    def destroy_current_popup(self) -> None:
        self.current_popup.destroy()

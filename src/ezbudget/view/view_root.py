import tkinter as tk
from typing import Protocol

from ezbudget.view import (
    Categories,
    CreateAccountPopUp,
    CreateCreditCardPopup,
    CreateIncomePopUp,
    IncomingOutgoing,
    RegisterLogin,
)
from ezbudget.view.view_transactions import Transactions

TITLE = "Ez Budget"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800


class Presenter(Protocol):
    def handle_register_user(self, event=None):
        ...

    def handle_login_user(self, event=None) -> None:
        ...

    def handle_create_account(self, event=None):
        ...

    def run(self) -> None:
        ...


class RootView(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(TITLE)
        self.resizable(False, False)
        self.presenter = None

        self.current_frame = None
        self.current_popup = None

        # Put the windows in the center of the screen
        # x_center = self.winfo_screenwidth() / 2 - WINDOW_WIDTH / 2
        # y_center = self.winfo_screenheight() / 2 - WINDOW_HEIGHT / 2
        # self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{int(x_center)}+{int(y_center)}")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

    def init_ui(self, presenter: Presenter) -> None:
        self.presenter = presenter

        self.show_register_login()
        # self.show_categories()
        # self.show_transactions()

    def error_message_set(self, target: str, message: str) -> None:
        if target == "frame":
            self.current_frame.error_message.set(message)
        else:
            self.current_popup.error_message.set(message)

    def get_user_data(self):
        return {
            "username": self.current_frame.username.get(),
            "password": self.current_frame.password.get(),
        }

    def get_account_data(self):
        return {
            "name": self.current_popup.account_name.get(),
            "account_type": "BANK",
            "initial_balance": self.current_popup.initial_balance.get(),
            "currency": self.current_popup.cbx_currency.get(),
        }

    def get_income_data(self):
        return {
            "name": self.current_popup.income_name.get(),
            "account_name": self.current_popup.cbx_target_account.get(),
            "expected_income_value": self.current_popup.expected_income.get(),
            "real_income_value": self.current_popup.real_income.get(),
            "income_day": self.current_popup.income_day.get(),
            "income_month": self.current_popup.cbx_income_month.get(),
            "recurrence": self.current_popup.cbx_recurrence.get(),
        }

    def get_credit_card_data(self):
        return {
            "name": self.current_popup.credit_card_name.get(),
            "account_type": "CARD",
            "initial_balance": self.current_popup.balance.get(),
            "credit_limit": self.current_popup.credit_limit.get(),
            "payment_day": self.current_popup.payment_day.get(),
            "interest_rate": self.current_popup.interest_rate.get(),
            "credit_method": self.current_popup.credit_method.get(),
            "currency": self.current_popup.cbx_currency.get(),
        }

    def show_register_login(self) -> None:
        self.current_frame = RegisterLogin(self, self.presenter)
        self.current_frame.pack(expand=True, fill="both")

    def show_incomig_outgoing(self, event=None) -> None:
        del event  # not used in this function
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = IncomingOutgoing(self, self.presenter)
        self.current_frame.refresh_accounts()
        self.current_frame.refresh_incomes()
        self.current_frame.refresh_credit_cards()
        self.current_frame.pack(expand=True, fill="both")

    def show_create_account_popup(self, event=None) -> None:
        del event  # not used in this function
        if self.current_popup:
            self.current_popup.destroy()
        self.current_popup = CreateAccountPopUp(self.current_frame, self.presenter)

    def show_create_income_popup(self, event=None) -> None:
        del event  # not used in this function
        if self.current_popup:
            self.current_popup.destroy()
        self.current_popup = CreateIncomePopUp(self.current_frame, self.presenter)

    def show_add_credit_popup(self, event=None) -> None:
        del event  # not used in this function
        if self.current_popup:
            self.current_popup.destroy()
        self.current_popup = CreateCreditCardPopup(self.current_frame, self.presenter)

    def show_categories(self, event=None) -> None:
        del event  # not used in this function
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = Categories(self, self.presenter)
        self.current_frame.pack(expand=True, fill="both")

    def show_transactions(self) -> None:
        self.current_frame = Transactions(self, self.presenter)
        self.current_frame.pack(expand=True, fill="both")

    def destroy_current_popup(self) -> None:
        self.current_popup.destroy()

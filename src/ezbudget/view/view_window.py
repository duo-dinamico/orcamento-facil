from datetime import datetime

import ttkbootstrap as ttk

from ezbudget.view import (
    Categories,
    CreateAccountPopUp,
    CreateCreditCardPopup,
    CreateIncomePopUp,
    HomePage,
    IncomingOutgoing,
    RegisterLogin,
    Transactions,
)

TITLE = "Ez Budget"
WINDOW_WIDTH = 2000
WINDOW_HEIGHT = 1400


class RootView(ttk.Window):
    def __init__(self) -> None:
        super().__init__(themename="flatly", title=TITLE, size=(WINDOW_WIDTH, WINDOW_HEIGHT), resizable=(False, False))
        self.presenter = None
        self.place_window_center()

        self.current_frame = None
        self.current_popup = None

    def init_ui(self, presenter) -> None:
        self.presenter = presenter
        self.show_register_login()

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
            "balance": self.current_popup.balance.get(),
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
            "balance": self.current_popup.balance.get(),
            "credit_limit": self.current_popup.credit_limit.get(),
            "payment_day": self.current_popup.payment_day.get(),
            "interest_rate": self.current_popup.interest_rate.get(),
            "credit_method": self.current_popup.credit_method.get(),
            "currency": self.current_popup.cbx_currency.get(),
        }

    def get_transaction_data(self):
        # TODO Strong date validation
        # Get datetime object
        date_obj = datetime.strptime(self.current_frame.dte_date.entry.get(), "%Y-%m-%d")

        # Get account id from the name that comes from Combobox
        account_id = self.presenter.get_account_id_by_name(self.current_frame.cbx_account.get())
        user_subcategory = self.current_frame.cbx_subcategory.get()
        split_category_subcategory = user_subcategory.split(" - ")
        subcategory_id = self.presenter.get_subcategory_id_by_name(split_category_subcategory[1])

        return {
            "account_id": account_id,
            "subcategory_id": subcategory_id,
            "date": date_obj,
            "value": self.current_frame.value.get(),
            "description": self.current_frame.description.get(),
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

    def show_update_transaction_popup(self, event=None) -> None:
        pass

    def show_categories(self, event=None) -> None:
        del event  # not used in this function
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = Categories(self, self.presenter)
        self.current_frame.refresh_categories()
        self.current_frame.refresh_selected_categories()
        self.current_frame.pack(expand=True, fill="both")

    def show_homepage(self, event=None) -> None:
        del event  # not used in this function
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = HomePage(self, self.presenter)
        self.current_frame.pack(expand=True, fill="both")

    def show_transactions(self, event=None) -> None:
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = Transactions(self, self.presenter)
        self.current_frame.pack(expand=True, fill="both")

    def destroy_current_popup(self) -> None:
        self.current_popup.destroy()

from datetime import datetime

import ttkbootstrap as ttk

from ezbudget.view import (
    Categories,
    CreateAccountPopUp,
    CreateCreditCardPopup,
    CreateIncomePopUp,
    CreateTransactionPopup,
    HomePage,
    IncomingOutgoing,
    RegisterLogin,
    Transactions,
)

TITLE = "Ez Budget"
# WINDOW_WIDTH = 1200
# WINDOW_HEIGHT = 800


class RootView(ttk.Window):
    def __init__(self) -> None:
        super().__init__(themename="flatly")
        self.title(TITLE)
        self.resizable(False, False)
        self.presenter = None

        self.current_frame = None
        self.current_popup = None

        # Put the windows in the center of the screen
        screen_width = self.winfo_screenwidth()
        window_width = int(screen_width / 1.5)
        x_center = screen_width / 2 - window_width / 2
        screen_height = self.winfo_screenheight()
        window_height = int(screen_height / 1.5)
        y_center = self.winfo_screenheight() / 2 - window_height / 2
        self.geometry(f"{window_width}x{window_height}+{int(x_center)}+{int(y_center)}")

    def init_ui(self, presenter) -> None:
        self.presenter = presenter

        # TODO Delete this
        self.presenter.login_dummy_data()

        self.show_register_login()
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

        # Join date
        month_value = self.presenter.get_month_value(self.current_popup.cbx_frame_date_month.get())
        date_str = (
            self.current_popup.cbx_frame_date_day.get()
            + "-"
            + str(month_value)
            + "-"
            + self.current_popup.cbx_frame_date_year.get()
        )

        # Get datetime object
        data_obj = datetime.strptime(date_str, "%m-%d-%Y").date()

        # Get account id from the name that comes from Combobox
        account_id = self.presenter.get_account_id_by_name(self.current_popup.cbx_account.get())

        return {
            "account_id": account_id,
            # "subcategory_id": self.current_popup.subcategory_id.get(),
            "subcategory_id": 1,
            "date": data_obj,
            "value": self.current_popup.value.get(),
            "description": self.current_popup.description.get(),
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

    def show_create_transaction_popup(self, event=None) -> None:
        del event  # not used in this function
        if self.current_popup:
            self.current_popup.destroy()
        self.current_popup = CreateTransactionPopup(self.current_frame, self.presenter)

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

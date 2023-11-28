import tkinter as tk

import ttkbootstrap as ttk


class CreateTransactionPopup(tk.Toplevel):
    """Class that creates the pop up window to create a transaction."""

    def __init__(self, parent, presenter) -> None:
        super().__init__(master=parent)

        self.transient(parent)
        self.resizable(False, False)
        self.title("Add Credit Card")

        self.error_message = tk.StringVar(value="")
        self.credit_card_name = tk.StringVar()
        self.balance = tk.StringVar()
        self.credit_limit = tk.StringVar()
        self.payment_day = tk.StringVar()
        self.interest_rate = tk.StringVar()
        self.credit_method = tk.StringVar()
        currencies = presenter.get_currency()

        lbl_credit_card_name = ttk.Label(self, text="Credit card name")
        lbl_credit_card_name.pack(anchor="w", padx=10, pady=5, fill="x")
        ent_credit_card_name = ttk.Entry(self, textvariable=self.credit_card_name)
        ent_credit_card_name.pack(anchor="w", padx=10, pady=5, fill="x")

        lbl_balance = ttk.Label(self, text="Initial balance")
        lbl_balance.pack(anchor="w", padx=10, pady=5, fill="x")
        ent_balance = ttk.Entry(self, textvariable=self.balance)
        ent_balance.pack(anchor="w", padx=10, pady=5, fill="x")

        lbl_currency = ttk.Label(self, text="Currency")
        lbl_currency.pack(anchor="w", padx=10, pady=5, fill="x")
        self.cbx_currency = ttk.Combobox(self, state="readonly", values=currencies)
        self.cbx_currency.current(0)
        self.cbx_currency.pack(anchor="w", padx=10, pady=5, fill="x")

        lbl_credit_limit = ttk.Label(self, text="Credit limit")
        lbl_credit_limit.pack(anchor="w", padx=10, pady=5, fill="x")
        ent_credit_limit = ttk.Entry(self, textvariable=self.credit_limit)
        ent_credit_limit.pack(anchor="w", padx=10, pady=5, fill="x")

        lbl_payment_day = ttk.Label(self, text="Repayment day")
        lbl_payment_day.pack(anchor="w", padx=10, pady=5, fill="x")
        ent_payment_day = ttk.Entry(self, textvariable=self.payment_day)
        ent_payment_day.pack(anchor="w", padx=10, pady=5, fill="x")

        lbl_interest_rate = ttk.Label(self, text="Interest rate")
        lbl_interest_rate.pack(anchor="w", padx=10, pady=5, fill="x")
        ent_interest_rate = ttk.Entry(self, textvariable=self.interest_rate)
        ent_interest_rate.pack(anchor="w", padx=10, pady=5, fill="x")

        lbl_credit_method = ttk.Label(self, text="Credit method")
        lbl_credit_method.pack(anchor="w", padx=10, pady=5, fill="x")
        ent_credit_method = ttk.Entry(self, textvariable=self.credit_method)
        ent_credit_method.pack(anchor="w", padx=10, pady=5, fill="x")

        lbl_error_popup = ttk.Label(self, textvariable=self.error_message)
        lbl_error_popup.pack(anchor="w", padx=10, pady=5, fill="x")

        btn_cancel = ttk.Button(self, text="Cancel", command=self.cancel_input, bootstyle="DANGER")
        btn_cancel.pack(side="left", padx=10, pady=5)
        btn_create_income = ttk.Button(self, text="Add credit card", bootstyle="SUCCESS")
        btn_create_income.pack(side="right", padx=10, pady=5)
        btn_create_income.bind("<Button-1>", presenter.handle_create_credit_card)
        # TODO this should enable us to confirm when we press enter
        # self.bind("<Return>", presenter.handle_create_income)

    def cancel_input(self):
        self.destroy()

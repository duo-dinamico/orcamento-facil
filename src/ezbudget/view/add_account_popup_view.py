import tkinter as tk
from tkinter import ttk


class AddAccountPopUp(tk.Toplevel):
    def __init__(self, parent, presenter) -> None:
        super().__init__(master=parent)

        self.transient(parent)
        self.resizable(False, False)
        self.title("Add account")

        self.account_name = tk.StringVar()
        self.initial_balance = tk.StringVar()
        self.error_message = tk.StringVar(value="")
        currencies = ["GBP", "EUR", "USD"]

        label_account_name = ttk.Label(self, text="Account name")
        label_account_name.pack(anchor="w", padx=10, pady=5, fill="x")
        entry_account_name = ttk.Entry(self, textvariable=self.account_name)
        entry_account_name.pack(anchor="w", padx=10, pady=5, fill="x")

        label_initial_balance = ttk.Label(self, text="Initial balance")
        label_initial_balance.pack(anchor="w", padx=10, pady=5, fill="x")
        entry_initial_balance = ttk.Entry(self, textvariable=self.initial_balance)
        entry_initial_balance.pack(anchor="w", padx=10, pady=5, fill="x")

        label_currency = ttk.Label(self, text="Currency")
        label_currency.pack(anchor="w", padx=10, pady=5, fill="x")
        currency_combobox = ttk.Combobox(self, state="readonly", values=currencies)
        currency_combobox.current(0)
        currency_combobox.pack(anchor="w", padx=10, pady=5, fill="x")

        label_error_popup = ttk.Label(self, textvariable=self.error_message)
        label_error_popup.pack(anchor="w", padx=10, pady=5, fill="x")

        button_cancel = ttk.Button(self, text="Cancel", command=self.cancel_input)
        button_cancel.pack(side="left", padx=10, pady=5)
        button_add_account = ttk.Button(self, text="Add account")
        button_add_account.pack(side="right", padx=10, pady=5)
        button_add_account.bind("<Button-1>", presenter.handle_add_account)

    def cancel_input(self):
        self.destroy()

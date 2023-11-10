import tkinter as tk
from tkinter import ttk


class AddAccountPopUp(tk.Toplevel):
    def __init__(self, parent, presenter) -> None:
        super().__init__(master=parent)

        self.parent = parent
        self.transient(parent)
        self.resizable(False, False)
        self.title("Add account")

        self.account_name = tk.StringVar()
        self.initial_balance = tk.StringVar()
        self.error_message = tk.StringVar(value="")
        self.currencies = ["GBP", "EUR", "USD"]

        self.label_account_name = ttk.Label(self, text="Account name")
        self.label_account_name.pack(anchor="w", padx=10, pady=5, fill="x")
        self.entry_account_name = ttk.Entry(self, textvariable=self.account_name)
        self.entry_account_name.pack(anchor="w", padx=10, pady=5, fill="x")

        self.label_initial_balance = ttk.Label(self, text="Initial balance")
        self.label_initial_balance.pack(anchor="w", padx=10, pady=5, fill="x")
        self.entry_initial_balance = ttk.Entry(self, textvariable=self.initial_balance)
        self.entry_initial_balance.pack(anchor="w", padx=10, pady=5, fill="x")

        self.label_currency = ttk.Label(self, text="Currency")
        self.label_currency.pack(anchor="w", padx=10, pady=5, fill="x")
        self.currency_combobox = ttk.Combobox(self, state="readonly", values=self.currencies)
        self.currency_combobox.current(0)
        self.currency_combobox.pack(anchor="w", padx=10, pady=5, fill="x")

        self.label_error_popup = ttk.Label(self, textvariable=self.error_message)
        self.label_error_popup.pack(anchor="w", padx=10, pady=5, fill="x")

        self.button_cancel = ttk.Button(self, text="Cancel", command=self.cancel_input)
        self.button_cancel.pack(side="left", padx=10, pady=5)
        self.button_add_account = ttk.Button(self, text="Add account")
        self.button_add_account.pack(side="right", padx=10, pady=5)
        self.button_add_account.bind("<Button-1>", presenter.handle_add_account)

    def cancel_input(self):
        self.destroy()

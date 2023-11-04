import tkinter as tk
from tkinter import ttk

from .utils.popup_setup import popup_setup


class AddAccountPopUp(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        popup_setup(self, parent, "Add account")

        self.fields = []
        self.account_name = tk.StringVar()
        self.account_name.trace_add("write", self.activate_add_account)
        self.initial_balance = tk.StringVar()
        self.initial_balance.trace_add("write", self.activate_add_account)
        self.currencies = ["GBP", "EUR", "USD"]

        frame_popup = ttk.Frame(self)
        frame_popup.pack(anchor="nw", fill="both", expand=True)

        self.currency_combobox = ttk.Combobox(frame_popup, state="readonly", values=self.currencies)
        self.currency_combobox.current(0)

        self.fields.extend(
            [
                ttk.Label(frame_popup, text="Account name"),
                ttk.Entry(frame_popup, textvariable=self.account_name),
                ttk.Label(frame_popup, text="Initial balance"),
                ttk.Entry(frame_popup, textvariable=self.initial_balance),
                ttk.Label(frame_popup, text="Currency"),
                self.currency_combobox,
            ]
        )

        for field in self.fields:
            field.pack(anchor="w", padx=10, pady=5, fill="x")

        ttk.Button(
            self,
            text="Cancel",
            command=self.cancel_input,
        ).pack(side="left", padx=10, pady=5)
        self.add_account = ttk.Button(
            self,
            text="Add account",
            state="disabled",
            command=lambda: self.parent.add_account(
                {
                    "account": self.account_name.get(),
                    "initial_balance": int(self.initial_balance.get()),
                    "currency": self.currency_combobox.get(),
                }
            ),
        )
        self.add_account.pack(side="right", padx=10, pady=5)

    def cancel_input(self):
        self.destroy()

    def activate_add_account(self, *args):
        account_name = self.account_name.get()
        initial_balance = self.initial_balance.get()
        if account_name != "" and initial_balance != 0:
            self.add_account.config(state="enabled")
        else:
            self.add_account.config(state="disabled")

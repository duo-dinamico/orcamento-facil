import tkinter as tk

import ttkbootstrap as ttk


class CreateAccountPopUp(tk.Toplevel):
    def __init__(self, parent, presenter) -> None:
        super().__init__(master=parent)

        self.transient(parent)
        self.resizable(False, False)
        self.title("Add account")

        self.account_name = tk.StringVar()
        self.initial_balance = tk.StringVar()
        self.error_message = tk.StringVar(value="")
        currencies = presenter.get_currency()

        lbl_account_name = ttk.Label(self, text="Account name")
        lbl_account_name.pack(anchor="w", padx=10, pady=5, fill="x")
        ent_account_name = ttk.Entry(self, textvariable=self.account_name)
        # TODO need to get the focus on account name entry somehow
        # ent_account_name.focus_set()
        ent_account_name.pack(anchor="w", padx=10, pady=5, fill="x")

        lbl_initial_balance = ttk.Label(self, text="Initial balance")
        lbl_initial_balance.pack(anchor="w", padx=10, pady=5, fill="x")
        ent_initial_balance = ttk.Entry(self, textvariable=self.initial_balance)
        ent_initial_balance.pack(anchor="w", padx=10, pady=5, fill="x")

        lbl_currency = ttk.Label(self, text="Currency")
        lbl_currency.pack(anchor="w", padx=10, pady=5, fill="x")
        self.cbx_currency = ttk.Combobox(self, state="readonly", values=currencies)
        self.cbx_currency.current(0)
        self.cbx_currency.pack(anchor="w", padx=10, pady=5, fill="x")

        lbl_error_popup = ttk.Label(self, textvariable=self.error_message)
        lbl_error_popup.pack(anchor="w", padx=10, pady=5, fill="x")

        btn_cancel = ttk.Button(self, text="Cancel", command=self.cancel_input, bootstyle="DANGER")
        btn_cancel.pack(side="left", padx=10, pady=5)
        btn_add_account = ttk.Button(self, text="Add account", bootstyle="SUCCESS")
        btn_add_account.pack(side="right", padx=10, pady=5)
        btn_add_account.bind("<Button-1>", presenter.handle_add_account)
        # TODO this should enable us to confirm when we press enter
        # self.bind("<Return>", presenter.handle_add_account)

    def cancel_input(self):
        self.destroy()

import tkinter as tk

import ttkbootstrap as ttk


class CreateTransactionPopup(tk.Toplevel):
    """A Toplevel window for the transaction creation."""

    def __init__(self, parent, presenter) -> None:
        """Construct the CreateTransactionPopup object.
        Parameters:
            parent: the id of the account where the transaction will be created.
            presenter: the id of the category of the transation.
        """
        super().__init__(master=parent)

        # Make this window a transient of is parent window
        self.transient(parent)

        self.resizable(False, False)
        self.title("Add New Transaction")

        # Define Class atributes
        self.error_message = tk.StringVar(value="")
        self.account_id = tk.StringVar()
        self.subcategory_id = tk.StringVar()
        self.transaction_date = tk.StringVar()
        self.value = tk.StringVar()
        self.description = tk.StringVar()

        # Get the account list
        accounts = presenter.get_account_list_by_user()

        # Get the subcategory list
        subcategories = presenter.get_subcategory_list_by_user()

        lbl_account = ttk.Label(self, text="Account")
        lbl_account.pack(anchor="w", padx=10, pady=5, fill="x")
        self.cbx_account = ttk.Combobox(self, state="readonly", values=accounts)
        self.cbx_account.current(0)
        self.cbx_account.pack(anchor="w", padx=10, pady=5, fill="x")

        lbl_subcategory = ttk.Label(self, text="Subcategory")
        lbl_subcategory.pack(anchor="w", padx=10, pady=5, fill="x")
        self.cbx_subcategory = ttk.Combobox(self, state="readonly", values=subcategories)
        self.cbx_subcategory.current(0)
        self.cbx_subcategory.pack(anchor="w", padx=10, pady=5, fill="x")

        lbl_transaction_date = ttk.Label(self, text="Date")
        lbl_transaction_date.pack(anchor="w", padx=10, pady=5, fill="x")
        ent_transaction_date = ttk.Entry(self, textvariable=self.transaction_date)
        ent_transaction_date.pack(anchor="w", padx=10, pady=5, fill="x")

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

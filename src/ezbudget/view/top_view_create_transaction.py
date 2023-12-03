import tkinter as tk

import ttkbootstrap as ttk


class CreateTransactionPopup(tk.Toplevel):
    """A Toplevel window for the transaction creation."""

    def __init__(self, parent, presenter) -> None:
        """Construct the CreateTransactionPopup object.

        Parameters:
            parent: the transaction frame.
            presenter: presenter of the aplication.
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
        self.transaction_date = tk.StringVar(value="01-01-23")
        self.cbx_frame_date_day = tk.StringVar(value="01")
        self.cbx_frame_date_month = tk.StringVar(value="01")
        self.cbx_frame_date_year = tk.StringVar(value="2023")
        self.value = tk.StringVar()
        self.description = tk.StringVar()

        # Get the account list
        accounts = presenter.get_account_list_by_user()

        # Get the subcategory list
        subcategories = presenter.get_subcategory_list()

        lbl_account = ttk.Label(self, text="Account")
        lbl_account.pack(anchor="w", padx=10, pady=5, fill="x")
        self.cbx_account = ttk.Combobox(self, state="readonly", values=accounts)

        # If the list is not empty, select first item
        if len(accounts) != 0:
            self.cbx_account.current(0)
        self.cbx_account.pack(anchor="w", padx=10, pady=5, fill="x")

        lbl_subcategory = ttk.Label(self, text="Subcategory")
        lbl_subcategory.pack(anchor="w", padx=10, pady=5, fill="x")
        self.cbx_subcategory = ttk.Combobox(self, state="readonly", values=subcategories)

        # If the list is not empty, select first item
        if len(subcategories) != 0:
            self.cbx_subcategory.current(0)
        self.cbx_subcategory.pack(anchor="w", padx=10, pady=5, fill="x")

        #
        # Create a frame just for the date
        #
        self.frame_date = ttk.LabelFrame(self, text="Date")
        self.frame_date.pack(anchor="w", padx=10, pady=5, fill="x")

        lbl_frame_date_day = ttk.Label(self.frame_date, text="Day")
        lbl_frame_date_day.pack(anchor="w", padx=10, pady=5, fill="x")
        self.cbx_frame_date_day = ttk.Combobox(self.frame_date, state="readonly", values=list(range(1, 32)))
        self.cbx_frame_date_day.pack(side="left")

        # Get month list
        month_list = presenter.get_month()

        lbl_frame_date_month = ttk.Label(self.frame_date, text="Month")
        lbl_frame_date_month.pack(anchor="w", padx=10, pady=5, fill="x")
        self.cbx_frame_date_month = ttk.Combobox(self.frame_date, state="readonly", values=month_list)
        self.cbx_frame_date_month.pack(side="left")

        lbl_frame_date_year = ttk.Label(self.frame_date, text="Year")
        lbl_frame_date_year.pack(anchor="w", padx=10, pady=5, fill="x")
        self.cbx_frame_date_year = ttk.Combobox(
            self.frame_date, state="readonly", values=list(range(2020, 2025))
        )  # TODO other years?!
        self.cbx_frame_date_year.pack(side="left")

        #
        # Date frame terminated
        #

        lbl_value = ttk.Label(self, text="Value")
        lbl_value.pack(anchor="w", padx=10, pady=5, fill="x")
        ent_value = ttk.Entry(self, textvariable=self.value)
        ent_value.pack(anchor="w", padx=10, pady=5, fill="x")

        lbl_description = ttk.Label(self, text="Description")
        lbl_description.pack(anchor="w", padx=10, pady=5, fill="x")
        ent_description = ttk.Entry(self, textvariable=self.description)
        ent_description.pack(anchor="w", padx=10, pady=5, fill="x")

        lbl_error_popup = ttk.Label(self, textvariable=self.error_message)
        lbl_error_popup.pack(anchor="w", padx=10, pady=5, fill="x")

        # Cancel button
        btn_cancel = ttk.Button(self, text="Cancel", command=self.cancel_input, bootstyle="DANGER")
        btn_cancel.pack(side="left", padx=10, pady=5)

        btn_create_transaction = ttk.Button(self, text="Add transaction", bootstyle="SUCCESS")
        btn_create_transaction.pack(side="right", padx=10, pady=5)
        btn_create_transaction.bind("<Button-1>", presenter.handle_create_transaction)

        # TODO this should enable us to confirm when we press enter
        # self.bind("<Return>", presenter.handle_create_income)

    def cancel_input(self):
        self.destroy()

import tkinter as tk

import ttkbootstrap as ttk
from sqlalchemy import Boolean


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
        lbl_frame_date_day.grid(row=0, column=0)
        self.cbx_frame_date_day = ttk.Combobox(self.frame_date, state="readonly", values=list(range(1, 32)))
        self.cbx_frame_date_day.current(0)
        self.cbx_frame_date_day.grid(row=1, column=0)

        # Get month list
        month_list = presenter.get_month()

        lbl_frame_date_month = ttk.Label(self.frame_date, text="Month")
        lbl_frame_date_month.grid(row=0, column=1)
        self.cbx_frame_date_month = ttk.Combobox(self.frame_date, state="readonly", values=month_list)
        self.cbx_frame_date_month.current(0)
        self.cbx_frame_date_month.grid(row=1, column=1)

        lbl_frame_date_year = ttk.Label(self.frame_date, text="Year")
        lbl_frame_date_year.grid(row=0, column=2)
        self.cbx_frame_date_year = ttk.Combobox(
            self.frame_date, state="readonly", values=list(range(2020, 2025))
        )  # TODO other years?!
        self.cbx_frame_date_year.current(0)
        self.cbx_frame_date_year.grid(row=1, column=2)

        #
        # Date frame terminated
        #

        lbl_value = ttk.Label(self, text="Value")
        lbl_value.pack(anchor="w", padx=10, pady=5, fill="x")

        # The validatecommand is a tupple with the method and a substitution code. %S is the char
        self.ent_value = ttk.Entry(
            self,
            textvariable=self.value,
            justify="right",
            validate="key",
            validatecommand=(self.register(self.check_value), "%S"),
        )
        self.ent_value.pack(anchor="w", padx=10, pady=5, fill="x")

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

    def check_value(self, char) -> Boolean:
        if char.isdigit() or char == ".":
            value_before_change = self.value.get()
            number_of_points = [x for x in value_before_change if x == "."]

            # Check if already have a point. Only can have one
            if char == "." and len(number_of_points) >= 1:
                print("JA TEM PONTO: ", number_of_points)
                return False

            # Check if we have two decimal, to add the point
            if len(value_before_change) == 1:
                value_with_point = "0." + self.value.get() + char
                self.value.set(value_with_point)

            # if we already have a point, then move it
            elif len(number_of_points) == 1:
                resultado = "".join(
                    (
                        value_before_change[:-3],
                        value_before_change[-2],
                        value_before_change[-3],
                        value_before_change[-1:],
                        char,
                    )
                )
                self.value.set(resultado)
                self.ent_value.icursor(len(resultado))
            return True
        else:
            return False

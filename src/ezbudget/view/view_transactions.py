import tkinter as tk
from datetime import datetime

import ttkbootstrap as ttk

from ezbudget.view import Header


class Transactions(ttk.Frame):
    """Class that creates the transactions view."""

    def __init__(self, parent, presenter) -> None:
        super().__init__(master=parent, bootstyle="secondary")
        self.presenter = presenter
        self.parent = parent

        # Define Class atributes
        self.error_message = tk.StringVar(value="")
        self.value = tk.StringVar()
        self.description = tk.StringVar()
        self.create_duplicate_btn = tk.StringVar(value="Add Transaction")

        # Get the account list
        accounts = presenter.get_account_list_by_user()
        # Get the subcategory list
        subcategories = presenter.get_user_subcategory_list()

        header = Header(self, self.presenter)
        header.pack(fill="x", ipady=10, padx=10, pady=(10, 5))

        frm_mid_section = ttk.Frame(self)
        frm_mid_section.pack(fill="both", expand=True, padx=10, pady=(5, 10))

        frm_mid_section.columnconfigure(0, weight=4)
        frm_mid_section.columnconfigure(1, weight=1)
        frm_mid_section.rowconfigure(0, weight=1)

        columns = ("Account", "Category", "Date", "Value", "Description")
        # Create the Treeview object with browse option so that only allow one selection
        self.tvw_transactions = ttk.Treeview(
            frm_mid_section, columns=columns, show="headings", selectmode="browse", bootstyle="secondary"
        )
        col_width = self.tvw_transactions.winfo_width() // len(columns)

        # Set the columns headers
        for i, col in enumerate(columns):
            self.tvw_transactions.column(col, anchor="center", width=col_width)
            self.tvw_transactions.heading(i, text=col)

        self.tvw_transactions.bind("<<TreeviewSelect>>", self.transaction_selected)

        self.tvw_transactions.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        frm_transaction_manage = ttk.Frame(frm_mid_section)
        frm_transaction_manage.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        lbl_account = ttk.Label(frm_transaction_manage, text="Account")
        lbl_account.pack(anchor="w", padx=10, pady=5, fill="x")
        self.cbx_account = ttk.Combobox(frm_transaction_manage, state="readonly", values=accounts)
        # If the list is not empty, select first item
        if len(accounts) != 0:
            self.cbx_account.current(0)
        self.cbx_account.pack(anchor="w", padx=5, pady=5, fill="x")

        lbl_subcategory = ttk.Label(frm_transaction_manage, text="Subcategory")
        lbl_subcategory.pack(anchor="w", padx=5, pady=5, fill="x")
        self.cbx_subcategory = ttk.Combobox(frm_transaction_manage, state="readonly", values=subcategories)

        # If the list is not empty, select first item
        if len(subcategories) != 0:
            self.cbx_subcategory.current(0)
        self.cbx_subcategory.pack(anchor="w", padx=5, pady=5, fill="x")

        # Date Entry
        lbl_date = ttk.Label(frm_transaction_manage, text="Date")
        lbl_date.pack(anchor="w", padx=5, pady=5, fill="x")

        self.dte_date = ttk.DateEntry(frm_transaction_manage, dateformat="%Y-%m-%d", bootstyle="primary")
        self.dte_date.pack(padx=5, pady=5, fill="x", expand=True)
        self.dte_date.entry.get()

        lbl_value = ttk.Label(frm_transaction_manage, text="Value")
        lbl_value.pack(anchor="w", padx=5, pady=5, fill="x")
        self.ent_value = ttk.Entry(frm_transaction_manage, textvariable=self.value, justify="right")
        self.ent_value.pack(padx=5, pady=5, fill="x", expand=True)

        lbl_description = ttk.Label(frm_transaction_manage, text="Description")
        lbl_description.pack(anchor="w", padx=5, pady=5, fill="x")
        ent_description = ttk.Entry(frm_transaction_manage, textvariable=self.description)
        ent_description.pack(padx=5, pady=5, fill="x", expand=True)

        lbl_error_popup = ttk.Label(frm_transaction_manage, textvariable=self.error_message)
        lbl_error_popup.pack(padx=5, pady=5, fill="x", expand=True)

        self.btn_create_transaction: ttk.Button | None = None
        self.btn_create_transaction = ttk.Button(frm_transaction_manage, textvariable=self.create_duplicate_btn)
        self.btn_create_transaction.pack(padx=5, pady=5, fill="x", expand=True)
        self.btn_create_transaction.bind("<Button-1>", self.presenter.handle_create_transaction)

        self.btn_update_transaction: ttk.Button | None = None
        self.btn_update_transaction = ttk.Button(frm_transaction_manage, text="Update Transaction", state="disabled")
        self.btn_update_transaction.pack(padx=5, pady=5, fill="x", expand=True)
        self.btn_update_transaction.bind("<Button-1>", self.parent.show_update_transaction_popup)

        self.btn_delete_transaction: ttk.Button | None = None
        self.btn_delete_transaction = ttk.Button(frm_transaction_manage, text="Delete Transaction", state="disabled")
        self.btn_delete_transaction.pack(padx=5, pady=5, fill="x", expand=True)
        self.btn_delete_transaction.bind("<Button-1>", self.delete_transaction)

        self.btn_clear_selection: ttk.Button | None = None
        self.btn_clear_selection = ttk.Button(frm_transaction_manage, text="Clear selection", state="disabled")
        self.btn_clear_selection.pack(padx=5, pady=5, fill="x", expand=True)
        self.btn_clear_selection.bind("<Button-1>", self.clear_selection)

        # Buttons
        self.btn_homepage: ttk.Button | None = None
        self.btn_homepage = ttk.Button(self, text="Go to homepage")
        self.btn_homepage.pack(padx=10, pady=(5, 10), side="bottom", fill="x")
        self.btn_homepage.bind("<Button-1>", self.parent.show_homepage)

        # Fill the Treeview with transactions
        self.refresh_transactions()

    def refresh_transactions(self):
        """Method that refresh the TreeView of transactions."""

        # Clear the Treeview
        for row in self.tvw_transactions.get_children():
            self.tvw_transactions.delete(row)

        # Get the transaction list from the presenter
        transactions_list = self.presenter.refresh_transactions_list()

        for item in transactions_list:
            transaction_date = f"{item.date.year}-{item.date.strftime('%m')}-{item.date.strftime('%d')}"
            self.tvw_transactions.insert(
                parent="",
                index="end",
                values=(
                    item.account.name,
                    f"{item.subcategory.category.name} - {item.subcategory.name}",
                    transaction_date,
                    item.value,
                    item.description,
                ),
            )

    def transaction_selected(self, event):
        if event.widget.selection():
            self.create_duplicate_btn.set("Duplicate Transaction")
            self.btn_clear_selection.configure(state="normal")
            tree = event.widget
            item_id = tree.selection()
            item = tree.item(item_id)
            if item["values"]:
                [account, category, date, value, description] = item["values"]
                for index, account_name in enumerate(self.cbx_account["values"]):
                    if account_name == account:
                        self.cbx_account.current(index)
                for index, category_name in enumerate(self.cbx_subcategory["values"]):
                    if category_name == category:
                        self.cbx_subcategory.current(index)
                self.dte_date.entry.delete(0, 10)
                self.dte_date.entry.insert(0, date)
                self.value.set(value)
                self.description.set(description)

    def delete_transaction(self, _):
        """Delete the selected transaction method."""

        # Get selected row
        row = self.tvw_transactions.focus()

        # Get the transaction_id of that row
        transaction_id = int(self.tvw_transactions.item(row).get("values")[0])

        # Call presenter method to delete transaction
        self.presenter.remove_transaction(transaction_id)

    def clear_selection(self, _):
        self.tvw_transactions.selection_set("")
        self.create_duplicate_btn.set("Add Transaction")
        self.btn_clear_selection.configure(state="disabled")
        self.cbx_account.current(0)
        self.cbx_subcategory.current(0)
        self.dte_date.entry.delete(0, 10)
        now = datetime.now()
        self.dte_date.entry.insert(0, now.strftime("%Y-%m-%d"))
        self.value.set("")
        self.description.set("")

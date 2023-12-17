import ttkbootstrap as ttk

from ezbudget.view import Header


class Transactions(ttk.Frame):
    """Class that creates the transactions view."""

    def __init__(self, parent, presenter) -> None:
        super().__init__(master=parent, bootstyle="secondary")
        self.presenter = presenter
        self.parent = parent

        header = Header(self, self.presenter)
        header.pack(fill="x", ipady=10, padx=10, pady=(10, 5))

        columns = ("Account", "Category", "Date", "Value", "Description")

        # Create the Treeview object with browse option so that only allow one selection
        self.tvw_transactions = ttk.Treeview(
            self, columns=columns, show="headings", selectmode="browse", bootstyle="secondary"
        )
        col_width = self.tvw_transactions.winfo_width() // len(columns)

        # Set the columns headers
        for i, col in enumerate(columns):
            self.tvw_transactions.column(col, anchor="center", width=col_width)
            self.tvw_transactions.heading(i, text=col, anchor="w")

        self.bind("<<TreeviewSelect>>", self.transaction_selected)

        self.tvw_transactions.pack(fill="both", expand=True, padx=10, pady=(5, 10))

        # Buttons
        self.go_back: ttk.Button | None = None
        self.go_back = ttk.Button(self, text="Go to homepage")
        self.go_back.pack(side="left", expand=True)
        self.go_back.bind("<Button-1>", self.parent.show_homepage)

        self.create_transaction_button: ttk.Button | None = None
        self.create_transaction_button = ttk.Button(self, text="Add Transaction")
        self.create_transaction_button.pack(side="left", expand=True)
        self.create_transaction_button.bind("<Button-1>", self.parent.show_create_transaction_popup)

        self.update_transaction_button: ttk.Button | None = None
        self.update_transaction_button = ttk.Button(self, text="Update Transaction")
        self.update_transaction_button.pack(side="left", expand=True)
        self.update_transaction_button.bind("<Button-1>", self.parent.show_update_transaction_popup)

        self.delete_transaction_button: ttk.Button | None = None
        self.delete_transaction_button = ttk.Button(self, text="Delete Transaction")
        self.delete_transaction_button.pack(side="left", expand=True)
        self.delete_transaction_button.bind("<Button-1>", self.delete_transaction)

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
            self.tvw_transactions.insert(
                parent="",
                index="end",
                values=(item.account.name, item.subcategory.name, item.date, item.value, item.description),
            )

    def transaction_selected(self):
        pass

    def delete_transaction(self, _):
        """Delete the selected transaction method."""

        # Get selected row
        row = self.tvw_transactions.focus()

        # Get the transaction_id of that row
        transaction_id = int(self.tvw_transactions.item(row).get("values")[0])

        # Call presenter method to delete transaction
        self.presenter.remove_transaction(transaction_id)

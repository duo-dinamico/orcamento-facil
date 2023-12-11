import ttkbootstrap as ttk


class Transactions(ttk.Frame):
    """Class that creates the transactions view."""

    def __init__(self, parent, presenter) -> None:
        super().__init__(master=parent)
        self.presenter = presenter
        self.parent = parent

        style = ttk.Style()
        style.configure("Treeview", font=(None, 11), rowheight=int(11 * 3))

        columns = ("ID", "Account", "Category", "Date", "Value", "Description")

        # Create the Treeview object with browse option so that only allow one selection
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse")

        # Set the columns headers
        for i, col in enumerate(columns):
            self.tree.heading(i, text=col, anchor="w")

        self.bind("<<TreeviewSelect>>", self.transaction_selected)

        self.tree.pack(fill="both", expand=True)

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
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Get the transaction list from the presenter
        transactions_list = self.presenter.refresh_transactions_list()

        for item in transactions_list:
            self.tree.insert(
                parent="",
                index="end",
                values=(item.id, item.account.name, item.subcategory_id, item.date, item.value, item.description),
            )

    def transaction_selected(self):
        pass

    def delete_transaction(self, _):
        """Delete the selected transaction method."""

        # Get selected row
        row = self.tree.focus()

        # Get the transaction_id of that row
        transaction_id = int(self.tree.item(row).get("values")[0])

        # Call presenter method to delete transaction
        self.presenter.remove_transaction(transaction_id)

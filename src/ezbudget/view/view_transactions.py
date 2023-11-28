import ttkbootstrap as ttk

columns = ("ID", "Account", "Category", "Date", "Value", "Description")


class Transactions(ttk.Frame):
    """Class that creates the transactions view."""

    def __init__(self, parent, presenter) -> None:
        super().__init__(master=parent)
        self.presenter = presenter
        self.parent = parent
        style = ttk.Style()
        style.configure("Treeview", font=(None, 11), rowheight=int(11 * 3))

        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        # Set the columns headers
        for i, col in enumerate(columns):
            self.tree.heading(i, text=col, anchor="w")

        self.bind("<<TreeviewSelect>>", self.transaction_selected)

        self.refresh_transactions_list()

        self.tree.pack(fill="both", expand=True)

        # Buttons
        self.create_transaction_button: ttk.Button | None = None
        self.create_transaction_button = ttk.Button(self, text="Add Transaction")
        self.create_transaction_button.pack()
        self.create_transaction_button.bind("<Button-1>", self.parent.show_create_transaction_popup)

    def refresh_transactions_list(self):
        """Method that refresh the TreeView of transactions."""
        transactions_list = self.presenter.refresh_transactions_list()
        # TODO in the future we'll need to clean the tree before adding
        for item in transactions_list:
            self.tree.insert(parent="", index="end", values=(item["id"], item["account_id"]))

    def transaction_selected(self):
        pass

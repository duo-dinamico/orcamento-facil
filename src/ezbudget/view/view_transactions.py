from tkinter import ttk

columns = ("ID", "Account", "Category", "Date", "Value", "Description")


class Transactions(ttk.Frame):
    """Class that creates the transactions view."""

    def __init__(self, parent, presenter) -> None:
        super().__init__(master=parent)
        self.presenter = presenter
        style = ttk.Style()
        style.configure("Treeview", font=(None, 11), rowheight=int(11 * 3))

        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        # Set the columns headers
        for i, col in enumerate(columns):
            self.tree.heading(i, text=col, anchor="w")

        self.bind("<<TreeviewSelect>>", self.transaction_selected)

        self.refresh_transactions_list()

        self.tree.pack(fill="both", expand=True)

    def refresh_transactions_list(self):
        transactions_list = self.presenter.refresh_transactions_list()
        print("XXXXXXXXXX: ", transactions_list)
        # TODO in the future we'll need to clean the tree before adding
        for item in transactions_list:
            print("Item:", item)
            self.tree.insert(parent="", index="end", values=(item["id"], item["account_id"]))

    def transaction_selected(self):
        pass

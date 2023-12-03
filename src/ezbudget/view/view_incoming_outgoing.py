import ttkbootstrap as ttk


class IncomingOutgoing(ttk.Frame):
    def __init__(self, parent, presenter) -> None:
        super().__init__(master=parent, bootstyle="secondary")
        self.parent = parent
        self.presenter = presenter

        self.accounts_tree: ttk.Treeview | None = None
        self.create_account_button: ttk.Button | None = None
        self.edit_account_button: ttk.Button | None = None
        self.delete_account_button: ttk.Button | None = None
        self.incomes_tree: ttk.Treeview | None = None
        self.create_income_button: ttk.Button | None = None
        self.edit_income_button: ttk.Button | None = None
        self.delete_income_button: ttk.Button | None = None
        self.credit_cards_tree: ttk.Treeview | None = None
        self.add_credit_card_button: ttk.Button | None = None
        self.edit_credit_card_button: ttk.Button | None = None
        self.delete_credit_card_button: ttk.Button | None = None

        # grid layout
        self.rowconfigure(0, weight=100)
        self.rowconfigure(1, weight=1)
        self.columnconfigure((0, 1, 2), weight=1)

        self.create_tree_widget("Account List", 0)
        self.create_tree_widget("Income List", 1)
        self.create_tree_widget("Credit Cards", 2)

        self.accounts_tree.bind("<<TreeviewSelect>>", self.account_selected)
        self.incomes_tree.bind("<<TreeviewSelect>>", self.income_selected)
        self.credit_cards_tree.bind("<<TreeviewSelect>>", self.credit_card_selected)

        self.create_account_button.bind("<Button-1>", self.parent.show_create_account_popup)
        self.create_income_button.bind("<Button-1>", self.parent.show_create_income_popup)
        self.add_credit_card_button.bind("<Button-1>", self.parent.show_add_credit_popup)

        self.next_button = ttk.Button(master=self, text="Choose your categories")
        self.next_button.grid(row=1, column=0, columnspan=3, sticky="sew", padx=(10, 10), pady=(0, 10))
        self.next_button.bind("<Button-1>", self.parent.show_categories)

    def create_tree_widget(self, title: str, column: int):
        frame = ttk.Frame(self, bootstyle="secondary")
        frame.grid(row=0, column=column, sticky="nsew", padx=(10, 10), pady=(10, 0))
        title_label = ttk.Label(
            frame, text=title, anchor="center", font=("Roboto", 14, "bold"), bootstyle="inverse-secondary"
        )
        title_label.pack(fill="x", pady=(5, 5))

        columns = ("name", "balance")
        tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode="browse", bootstyle="light")

        # define headings
        tree.heading("name", text="Name")
        tree.heading("balance", text="Balance")

        tree.pack(fill="both", expand=True)

        add_button = ttk.Button(frame, text="Add", bootstyle="dark")
        add_button.pack(fill="x", pady=(5, 5))
        edit_button = ttk.Button(frame, text="Edit", state="disabled", bootstyle="dark")
        edit_button.pack(fill="x", pady=(5, 5))
        delete_button = ttk.Button(frame, text="Delete", state="disabled", bootstyle="dark")
        delete_button.pack(fill="x", pady=(5, 5))

        match column:
            case 0:
                setattr(self, "accounts_tree", tree)
                setattr(self, "create_account_button", add_button)
                setattr(self, "edit_account_button", edit_button)
                setattr(self, "delete_account_button", delete_button)
            case 1:
                setattr(self, "incomes_tree", tree)
                setattr(self, "create_income_button", add_button)
                setattr(self, "edit_income_button", edit_button)
                setattr(self, "delete_income_button", delete_button)
            case 2:
                setattr(self, "credit_cards_tree", tree)
                setattr(self, "add_credit_card_button", add_button)
                setattr(self, "edit_credit_card_button", edit_button)
                setattr(self, "delete_credit_card_button", delete_button)

    def account_selected(self, event):
        del event  # not used in this function
        self.edit_account_button.config(state="enabled")
        self.delete_account_button.config(state="enabled")
        return self.accounts_tree.selection()

    def income_selected(self, event):
        del event  # not used in this function
        self.edit_income_button.config(state="enabled")
        self.delete_income_button.config(state="enabled")
        return self.incomes_tree.selection()

    def credit_card_selected(self, event):
        del event  # not used in this function
        self.edit_credit_card_button.config(state="enabled")
        self.delete_credit_card_button.config(state="enabled")
        return self.credit_cards_tree.selection()

    def refresh_accounts(self):
        account_list = self.presenter.refresh_account_list()
        # TODO in the future we'll need to clean the tree before adding
        for item in account_list:
            self.accounts_tree.insert(parent="", index="end", iid=item.id, values=(item.name, item.balance))

    def refresh_incomes(self):
        income_list = self.presenter.refresh_income_list()
        # TODO in the future we'll need to clean the tree before adding
        for item in income_list:
            self.incomes_tree.insert(
                parent="", index="end", iid=item.id, values=(item.name, item.expected_income_value)
            )

    def refresh_credit_cards(self):
        credit_card_list = self.presenter.refresh_credit_card_list()
        # TODO in the future we'll need to clean the tree before adding
        for item in credit_card_list:
            self.credit_cards_tree.insert(parent="", index="end", iid=item.id, values=(item.name, item.balance))

    def create_account(self, account):
        self.accounts_tree.insert(
            parent="",
            index="end",
            iid=account.id,
            values=(account.name, account.balance),
        )

    def create_income(self, income):
        self.incomes_tree.insert(
            parent="",
            index="end",
            iid=income.id,
            values=(income.name, income.real_income_value),
        )

    def add_credit_card(self, credit_card):
        self.credit_cards_tree.insert(
            parent="",
            index="end",
            iid=credit_card.id,
            values=(credit_card.name, credit_card.balance),
        )

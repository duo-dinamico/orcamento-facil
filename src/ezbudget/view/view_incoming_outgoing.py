import ttkbootstrap as ttk

from ezbudget.view import Header


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
        self.rowconfigure((0, 2), weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure((0, 1, 2), weight=1)

        header = Header(self, self.presenter)
        header.grid(sticky="ew", row=0, column=0, columnspan=3, ipady=10, padx=10, pady=(10, 5))

        self.frm_account_list = ttk.Frame(self)
        self.frm_account_list.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=5)
        self.frm_income_list = ttk.Frame(self)
        self.frm_income_list.grid(row=1, column=1, sticky="nsew", padx=(5, 5), pady=5)
        self.frm_credit_cards = ttk.Frame(self)
        self.frm_credit_cards.grid(row=1, column=2, sticky="nsew", padx=(5, 10), pady=5)

        self.create_tree_widget("Account List", self.frm_account_list)
        self.create_tree_widget("Income List", self.frm_income_list)
        self.create_tree_widget("Credit Cards", self.frm_credit_cards)

        self.accounts_tree.bind("<<TreeviewSelect>>", self.account_selected)
        self.incomes_tree.bind("<<TreeviewSelect>>", self.income_selected)
        self.credit_cards_tree.bind("<<TreeviewSelect>>", self.credit_card_selected)

        self.create_account_button.bind("<Button-1>", self.parent.show_create_account_popup)
        self.create_income_button.bind("<Button-1>", self.parent.show_create_income_popup)
        self.add_credit_card_button.bind("<Button-1>", self.parent.show_add_credit_popup)

        btn_show_homepage = ttk.Button(master=self, text="Return to Homepage")
        btn_show_homepage.grid(row=2, column=0, columnspan=3, sticky="sew", padx=(10, 10), pady=(0, 10))
        btn_show_homepage.bind("<Button-1>", self.parent.show_homepage)

    def create_tree_widget(self, title: str, frame):
        lbl_title = ttk.Label(frame, text=title, font=("Roboto", 14, "bold"))
        lbl_title.pack(fill="x", padx=5, pady=(5, 0))

        columns = ("name", "balance")
        tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode="browse", bootstyle="secondary")

        # define headings
        tree.heading("name", text="Name")
        tree.heading("balance", text="Balance")
        col_width = tree.winfo_width() // 2
        tree.column("name", anchor="center", width=col_width)
        tree.column("balance", anchor="center", width=col_width)

        tree.pack(fill="both", expand=True, padx=5, pady=(5, 0))

        add_button = ttk.Button(frame, text="Add")
        add_button.pack(side="left", fill="x", expand=True, padx=(5, 0), pady=5)
        edit_button = ttk.Button(frame, text="Edit", state="disabled")
        edit_button.pack(side="left", fill="x", expand=True, padx=(5, 5), pady=5)
        delete_button = ttk.Button(frame, text="Delete", state="disabled")
        delete_button.pack(side="left", fill="x", expand=True, padx=(0, 5), pady=5)

        match title:
            case "Account List":
                setattr(self, "accounts_tree", tree)
                setattr(self, "create_account_button", add_button)
                setattr(self, "edit_account_button", edit_button)
                setattr(self, "delete_account_button", delete_button)
            case "Income List":
                setattr(self, "incomes_tree", tree)
                setattr(self, "create_income_button", add_button)
                setattr(self, "edit_income_button", edit_button)
                setattr(self, "delete_income_button", delete_button)
            case "Credit Cards":
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

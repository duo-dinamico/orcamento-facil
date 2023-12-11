import ttkbootstrap as ttk


class HomePage(ttk.Frame):
    def __init__(self, parent, presenter) -> None:
        super().__init__(master=parent, bootstyle="secondary")
        self.parent = parent
        self.presenter = presenter

        username = self.set_username()

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        ttk.Label(self, text=f" Hello {username}!", font=("Roboto", 14, "bold")).grid(
            sticky="ew", row=0, column=0, columnspan=3, ipady=10, padx=10, pady=(10, 5)
        )

        frm_balances = ttk.Frame(self)
        frm_balances.grid(sticky="nsew", row=1, column=0, padx=(10, 5), pady=(5, 10))
        ttk.Label(frm_balances, text="Bank and Credit Card Balances", font=("Roboto", 14, "bold")).pack(
            fill="x", padx=5, pady=(5, 0)
        )
        self.tvw_accounts = ttk.Treeview(
            frm_balances, columns=("name", "total"), show="headings", selectmode="none", bootstyle="secondary"
        )
        self.tvw_accounts.heading("name", text=" ")
        self.tvw_accounts.heading("total", text="Total")
        self.tvw_accounts.column("total", anchor="center")
        self.tvw_accounts.tag_configure("parent", font=("Roboto", 11, "bold"))
        self.refresh_total_and_accounts()
        self.tvw_accounts.pack(fill="both", expand=True, padx=5, pady=(5, 0))

        frm_buttons = ttk.Frame(frm_balances)
        frm_buttons.pack(fill="x", side="bottom")
        btn_manage_incoming_outgoing = ttk.Button(frm_buttons, text="Manage Accounts and Sources")
        btn_manage_incoming_outgoing.pack(fill="x", padx=5, pady=(5, 0))
        btn_manage_incoming_outgoing.bind("<Button-1>", self.parent.show_incomig_outgoing)
        btn_manage_categories = ttk.Button(frm_buttons, text="Manage Categories")
        btn_manage_categories.pack(fill="x", padx=5, pady=(5, 5))
        btn_manage_categories.bind("<Button-1>", self.parent.show_categories)
        btn_add_transaction = ttk.Button(frm_buttons, text="Manage Transactions")
        btn_add_transaction.pack(fill="x", padx=5, pady=(0, 5))

        ttk.Label(frm_balances, text="Credit Cards", font=("Roboto", 14, "bold")).pack(fill="x", padx=5, pady=(5, 0))
        self.tvw_credit_cards = ttk.Treeview(
            frm_balances, columns=("name", "total"), show="headings", selectmode="none", bootstyle="secondary"
        )
        self.tvw_credit_cards.heading("name", text=" ")
        self.tvw_credit_cards.heading("total", text="Total")
        self.tvw_credit_cards.column("total", anchor="center")
        self.tvw_credit_cards.tag_configure("parent", font=("Roboto", 11, "bold"))
        self.refresh_total_and_credit_cards()
        self.tvw_credit_cards.pack(fill="both", expand=True, padx=5, pady=(5, 0))

        frm_budgeted_balance = ttk.Frame(self)
        frm_budgeted_balance.grid(sticky="nsew", row=1, column=1, padx=(5, 10), pady=(5, 10))

        ttk.Label(frm_budgeted_balance, text="Budgeted Balance", font=("Roboto", 14, "bold")).pack(
            fill="x", padx=5, pady=(5, 0)
        )

    def set_username(self):
        return self.presenter.handle_set_username()

    def refresh_total_and_accounts(self):
        for item in self.tvw_accounts.get_children():
            self.tvw_accounts.delete(item)
        total_balance_and_user_accounts = self.presenter.handle_set_total_accounts()
        self.tvw_accounts.insert(
            "",
            "end",
            open=True,
            iid=1,
            tags="parent",
            values=("Sum of all accounts", total_balance_and_user_accounts["balance"]),
        )
        for account in total_balance_and_user_accounts["user_accounts"]:
            self.tvw_accounts.insert(
                1, "end", iid=f"account {account.id}", values=(f"    {account.name}", account.balance)
            )

    def refresh_total_and_credit_cards(self):
        for item in self.tvw_credit_cards.get_children():
            self.tvw_credit_cards.delete(item)
        total_balance_and_user_cards = self.presenter.handle_set_total_credit_cards()
        self.tvw_credit_cards.insert(
            "",
            "end",
            open=True,
            iid=1,
            tags="parent",
            values=("Sum of all cards", total_balance_and_user_cards["balance"]),
        )
        for card in total_balance_and_user_cards["user_cards"]:
            self.tvw_credit_cards.insert(1, "end", iid=f"card {card.id}", values=(f"    {card.name}", card.balance))

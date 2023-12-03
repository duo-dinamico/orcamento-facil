import ttkbootstrap as ttk


class HomePage(ttk.Frame):
    def __init__(self, parent, presenter) -> None:
        super().__init__(master=parent, bootstyle="secondary")
        self.parent = parent
        self.presenter = presenter

        username = self.set_username()

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure((0, 1, 2), weight=1)

        ttk.Label(self, text=f" Hello {username}!", font=("Roboto", 14, "bold")).grid(
            sticky="ew", row=0, column=0, columnspan=3, ipady=10, padx=10, pady=(10, 0)
        )

        frm_balance = ttk.Frame(self)
        frm_balance.grid(sticky="nsew", row=1, column=0, padx=(10, 0), pady=(5, 10))
        ttk.Label(frm_balance, text="Balance", font=("Roboto", 14, "bold")).pack(fill="x", padx=5, pady=(5, 0))
        self.tvw_accounts = ttk.Treeview(
            frm_balance, columns=("name", "total"), show="headings", selectmode="none", bootstyle="secondary"
        )
        self.tvw_accounts.heading("name", text=" ")
        self.tvw_accounts.heading("total", text="Total")
        self.tvw_accounts.column("total", anchor="center")
        self.tvw_accounts.tag_configure("parent", font=("Roboto", 11, "bold"))
        self.refresh_total_and_accounts()
        self.tvw_accounts.pack(fill="both", expand=True, padx=5, pady=(5, 0))

        frm_buttons = ttk.Frame(frm_balance)
        frm_buttons.pack(fill="x", side="bottom")
        btn_add_account = ttk.Button(frm_buttons, text="Add an account")
        btn_add_account.pack(fill="x", padx=5, pady=(5, 0))
        btn_add_account.bind("<Button-1>", self.parent.show_create_account_popup)
        btn_add_transaction = ttk.Button(frm_buttons, text="Add a transaction")
        btn_add_transaction.pack(fill="x", padx=5, pady=5)

        frm_credit_cards = ttk.Frame(self)
        frm_credit_cards.grid(sticky="nsew", row=1, column=1, padx=5, pady=(5, 10))

        ttk.Label(frm_credit_cards, text="Credit Cards", font=("Roboto", 14, "bold")).pack(
            fill="x", padx=5, pady=(5, 0)
        )

        frm_budgeted_balance = ttk.Frame(self)
        frm_budgeted_balance.grid(sticky="nsew", row=1, column=2, padx=(0, 10), pady=(5, 10))

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

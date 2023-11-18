from tkinter import ttk


class IncomingOutgoing(ttk.Frame):
    def __init__(self, parent, presenter) -> None:
        super().__init__(master=parent)
        self.parent = parent
        self.presenter = presenter

        style = ttk.Style()
        # style.configure("Treeview.Heading", font=(None, 14), rowheight=int(14 * 2.5))
        style.configure("Treeview", font=(None, 11), rowheight=int(11 * 3))

        self.accounts_tree: ttk.Treeview | None = None
        self.add_account_button: ttk.Button | None = None
        self.edit_account_button: ttk.Button | None = None
        self.delete_account_button: ttk.Button | None = None
        self.incomes_tree: ttk.Treeview | None = None
        self.add_income_button: ttk.Button | None = None
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
        self.add_account_button.bind("<Button-1>", self.parent.show_add_account_popup)
        self.add_income_button.bind("<Button-1>", self.parent.show_add_income_popup)

        self.next_button = ttk.Button(master=self, text="Next")
        self.next_button.grid(row=1, column=0, columnspan=3, sticky="sew", padx=(10, 10), pady=(0, 10))

    def create_tree_widget(self, title: str, column: int):
        frame = ttk.Frame(self)
        frame.grid(row=0, column=column, sticky="nsew", padx=(10, 10), pady=(10, 0))
        title_label = ttk.Label(frame, text=title, anchor="center")
        title_label.pack(fill="x", pady=(5, 5))

        columns = ("name", "balance")
        tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode="browse", style="Treeview")

        # define headings
        tree.heading("name", text="Name")
        tree.heading("balance", text="Balance")

        tree.pack(fill="both", expand=True)

        add_button = ttk.Button(frame, text="Add")
        add_button.pack(fill="x", pady=(5, 5))
        edit_button = ttk.Button(frame, text="Edit", state="disabled")
        edit_button.pack(fill="x", pady=(5, 5))
        delete_button = ttk.Button(frame, text="Delete", state="disabled")
        delete_button.pack(fill="x", pady=(5, 5))

        match column:
            case 0:
                setattr(self, "accounts_tree", tree)
                setattr(self, "add_account_button", add_button)
                setattr(self, "edit_account_button", edit_button)
                setattr(self, "delete_account_button", delete_button)
            case 1:
                setattr(self, "incomes_tree", tree)
                setattr(self, "add_income_button", add_button)
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

    def refresh_accounts(self):
        account_list = self.presenter.refresh_account_list()
        for item in account_list:
            self.accounts_tree.insert(parent="", index="end", iid=item.id, values=(item.name, item.initial_balance))

    def add_account(self, account):
        self.accounts_tree.insert(
            parent="",
            index="end",
            iid=account.id,
            values=(account.name, account.initial_balance),
        )

        # variables
        # self.paddings = {"padx": 10, "pady": 5}
        # self.fields = []
        # self.accounts = []
        # self.incomes = []
        # self.credit_cards = []
        # self.line_widgets = []
        # self.line_widgets_incomes = []
        # self.line_widgets_credit_cards = []
        # self.frames_left = {}
        # self.frames_right = {}

        # styling
        # self.style = ttk.Style()
        # self.style.configure("Red.TButton", background="red4", relief="raised")

        # Here starts the frame listing and building
        # self.frames_left["personal_info"] = ttk.LabelFrame(
        #     self, text="Personal info", relief="ridge"
        # )
        # self.frames_left["adding_details"] = ttk.LabelFrame(
        #     self, text="Adding details", relief="ridge"
        # )
        # self.frames_right["account_list"] = ttk.LabelFrame(
        #     self, text="Account list", relief="ridge"
        # )
        # self.frames_right["income_list"] = ttk.LabelFrame(self, text="Income list", relief="ridge")
        # self.frames_right["credit_cards"] = ttk.LabelFrame(
        #     self, text="Credit cards list", relief="ridge"
        # )

        # for index, frame in enumerate(self.frames_left.values()):
        #     frame.grid(**self.paddings, column=0, row=index, sticky="nsew")
        # for index, frame in enumerate(self.frames_right.values()):
        #     frame.grid(**self.paddings, column=1, row=index, sticky="nsew")

        # Here starts the field listing and building
        # self.nome = tk.StringVar()
        # self.password = tk.StringVar()
        # self.information = tk.StringVar(value="Information.")
        # self.add_account_button = ttk.Button(
        #     self.frames_left["adding_details"],
        #     text="Add account",
        #     state="disabled",
        # )
        # self.add_income_button = ttk.Button(
        #     self.frames_left["adding_details"],
        #     text="Add income source",
        #     state="disabled",
        # )
        # self.add_credit_card_button = ttk.Button(
        #     self.frames_left["adding_details"],
        #     text="Add credit card",
        #     state="disabled",
        # )
        # self.fields.extend(
        #     [
        #         ttk.Label(self.frames_left["personal_info"], text="Name"),
        #         ttk.Entry(self.frames_left["personal_info"], textvariable=self.nome),
        #         ttk.Label(self.frames_left["personal_info"], text="Password"),
        #         ttk.Entry(self.frames_left["personal_info"], show="*", textvariable=self.password),
        #         ttk.Button(
        #             self.frames_left["personal_info"],
        #             text="Add user",
        #         ),
        #         ttk.Button(
        #             self.frames_left["personal_info"],
        #             text="Login",
        #         ),
        #         ttk.Button(
        #             self.frames_left["personal_info"],
        #             text="Logout",
        #         ),
        #         ttk.Label(self.frames_left["personal_info"], textvariable=self.information),
        #         self.add_account_button,
        #         self.add_income_button,
        #         self.add_credit_card_button,
        #     ]
        # )
        # for field in self.fields:
        #     field.pack(**self.paddings, anchor="w", fill="x")

        # self.titles = []
        # self.titles.extend(
        #     [
        #         ttk.Label(self.frames_right["account_list"], text="Account name"),
        #         ttk.Label(self.frames_right["account_list"], text="Initial balance"),
        #         ttk.Label(self.frames_right["account_list"], text="Delete"),
        #     ]
        # )
        # for index, title in enumerate(self.titles):
        #     title.grid(**self.paddings, column=index, row=0, sticky="n")

        # self.titles_income = []
        # self.titles_income.extend(
        #     [
        #         ttk.Label(self.frames_right["income_list"], text="Income name"),
        #         ttk.Label(self.frames_right["income_list"], text="Predicted income"),
        #         ttk.Label(self.frames_right["income_list"], text="Delete"),
        #     ]
        # )
        # for index, title in enumerate(self.titles_income):
        #     title.grid(**self.paddings, column=index, row=0, sticky="n")

        # self.titles_credit_cards = []
        # self.titles_credit_cards.extend(
        #     [
        #         ttk.Label(self.frames_right["credit_cards"], text="Credit card name"),
        #         ttk.Label(self.frames_right["credit_cards"], text="Current balance"),
        #         ttk.Label(self.frames_right["credit_cards"], text="Delete"),
        #     ]
        # )
        # for index, title in enumerate(self.titles_credit_cards):
        #     title.grid(**self.paddings, column=index, row=0, sticky="n")

        # self.next_button = ttk.Button(
        #     self,
        #     text="Next",
        #     state="disabled",
        # )
        # self.next_button.grid(column=0, row=3, columnspan=2, pady=5, padx=5, sticky="ew")

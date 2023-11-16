from tkinter import ttk


def column_title_component(parent, text_label_frame: str, text_button_frame: str, handler):
    label_frame = ttk.LabelFrame(master=parent, text=text_label_frame, relief="ridge")
    label_frame.pack(expand=True, fill="both")
    label_frame.columnconfigure((0, 1, 2), weight=8)
    label_frame.columnconfigure(3, weight=1)

    label_title_name = ttk.Label(label_frame, text="Name", anchor="center")
    label_title_name.grid(row=0, column=0, sticky="new", padx=(5, 0), pady=(5, 5))
    label_title_balance = ttk.Label(label_frame, text="Balance", anchor="center")
    label_title_balance.grid(row=0, column=1, sticky="new", padx=(5, 5), pady=(5, 5))
    label_title_delete = ttk.Label(label_frame, text="Delete", anchor="center")
    label_title_delete.grid(row=0, column=2, sticky="new", padx=(0, 5), pady=(5, 5))

    add_button = ttk.Button(master=parent, text=text_button_frame)
    add_button.pack(fill="x", anchor="s", pady=(15, 0))
    add_button.bind("<Button-1>", handler)

    return label_frame


class StartingView(ttk.Frame):
    def __init__(self, parent, presenter) -> None:
        super().__init__(master=parent)
        self.parent = parent
        self.presenter = presenter

        # grid layout
        self.rowconfigure(0, weight=12)
        self.rowconfigure(1, weight=1)
        self.columnconfigure((0, 1, 2), weight=1)

        self.accounts_widgets = []

        self.accounts_frame = ttk.Frame(master=self)
        self.accounts_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=(10, 0))
        self.accounts = column_title_component(
            self.accounts_frame, "Accounts list", "Add account", self.parent.show_add_account_popup
        )

        self.incomes_frame = ttk.Frame(master=self)
        self.incomes_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 10), pady=(10, 0))
        self.incomes = column_title_component(
            self.incomes_frame, "Income list", "Add income", self.presenter.handle_add_account
        )

        self.credit_cards_frame = ttk.Frame(master=self)
        self.credit_cards_frame.grid(row=0, column=2, sticky="nsew", padx=(0, 10), pady=(10, 0))
        self.credit_cards = column_title_component(
            self.credit_cards_frame, "Credit cards", "Add credit card", self.presenter.handle_add_account
        )

        self.next_button = ttk.Button(master=self, text="Next")
        self.next_button.grid(row=1, column=0, columnspan=3, sticky="ew", padx=(10, 10))

    def refresh_accounts(self):
        self.presenter.refresh_account_list()

    def refresh_accounts_widgets(self, account_list: list):
        for widget in self.accounts_widgets:
            widget.destroy()
        for i, item in enumerate(account_list):
            account_label = ttk.Label(self.accounts, text=item.name)
            balance_label = ttk.Label(self.accounts, text=item.initial_balance)
            delete_button = ttk.Button(
                self.accounts,
                text=item.id,
                width=4,
                # command=lambda item=item: self.delete_account(item.id),
            )

            account_label.grid(column=0, row=i + 1, sticky="new", padx=(10, 0), pady=(10, 0))
            balance_label.grid(column=1, row=i + 1, sticky="new", padx=(10, 0), pady=(10, 0))
            delete_button.grid(column=2, row=i + 1, sticky="new", padx=(10, 0), pady=(10, 0))

            self.accounts_widgets.extend([account_label, balance_label, delete_button])

        scroll = ttk.Scrollbar(master=self.accounts, orient="vertical")
        scroll.grid(column=3, row=0, rowspan=len(self.accounts_widgets), sticky="nse")

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

import tkinter as tk
from tkinter import ttk


class StartingView(ttk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(master=parent)

        # variables
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=4)
        self.rowconfigure(1, weight=4)
        self.rowconfigure(2, weight=4)
        self.rowconfigure(3, weight=1)
        self.paddings = {"padx": 10, "pady": 5}
        self.fields = []
        self.accounts = []
        self.incomes = []
        self.credit_cards = []
        self.line_widgets = []
        self.line_widgets_incomes = []
        self.line_widgets_credit_cards = []
        self.frames_left = {}
        self.frames_right = {}

        # styling
        self.style = ttk.Style()
        self.style.configure("Red.TButton", background="red4", relief="raised")

        # Here starts the frame listing and building
        self.frames_left["personal_info"] = ttk.LabelFrame(
            self, text="Personal info", relief="ridge"
        )
        self.frames_left["adding_details"] = ttk.LabelFrame(
            self, text="Adding details", relief="ridge"
        )
        self.frames_right["account_list"] = ttk.LabelFrame(
            self, text="Account list", relief="ridge"
        )
        self.frames_right["income_list"] = ttk.LabelFrame(self, text="Income list", relief="ridge")
        self.frames_right["credit_cards"] = ttk.LabelFrame(
            self, text="Credit cards list", relief="ridge"
        )

        for index, frame in enumerate(self.frames_left.values()):
            frame.grid(**self.paddings, column=0, row=index, sticky="nsew")
        for index, frame in enumerate(self.frames_right.values()):
            frame.grid(**self.paddings, column=1, row=index, sticky="nsew")

        # Here starts the field listing and building
        self.nome = tk.StringVar()
        self.password = tk.StringVar()
        self.information = tk.StringVar(value="Information.")
        self.add_account_button = ttk.Button(
            self.frames_left["adding_details"],
            text="Add account",
            state="disabled",
        )
        self.add_income_button = ttk.Button(
            self.frames_left["adding_details"],
            text="Add income source",
            state="disabled",
        )
        self.add_credit_card_button = ttk.Button(
            self.frames_left["adding_details"],
            text="Add credit card",
            state="disabled",
        )
        self.fields.extend(
            [
                ttk.Label(self.frames_left["personal_info"], text="Name"),
                ttk.Entry(self.frames_left["personal_info"], textvariable=self.nome),
                ttk.Label(self.frames_left["personal_info"], text="Password"),
                ttk.Entry(self.frames_left["personal_info"], show="*", textvariable=self.password),
                ttk.Button(
                    self.frames_left["personal_info"],
                    text="Add user",
                ),
                ttk.Button(
                    self.frames_left["personal_info"],
                    text="Login",
                ),
                ttk.Button(
                    self.frames_left["personal_info"],
                    text="Logout",
                ),
                ttk.Label(self.frames_left["personal_info"], textvariable=self.information),
                self.add_account_button,
                self.add_income_button,
                self.add_credit_card_button,
            ]
        )
        for field in self.fields:
            field.pack(**self.paddings, anchor="w", fill="x")

        self.titles = []
        self.titles.extend(
            [
                ttk.Label(self.frames_right["account_list"], text="Account name"),
                ttk.Label(self.frames_right["account_list"], text="Initial balance"),
                ttk.Label(self.frames_right["account_list"], text="Delete"),
            ]
        )
        for index, title in enumerate(self.titles):
            title.grid(**self.paddings, column=index, row=0, sticky="n")

        self.titles_income = []
        self.titles_income.extend(
            [
                ttk.Label(self.frames_right["income_list"], text="Income name"),
                ttk.Label(self.frames_right["income_list"], text="Predicted income"),
                ttk.Label(self.frames_right["income_list"], text="Delete"),
            ]
        )
        for index, title in enumerate(self.titles_income):
            title.grid(**self.paddings, column=index, row=0, sticky="n")

        self.titles_credit_cards = []
        self.titles_credit_cards.extend(
            [
                ttk.Label(self.frames_right["credit_cards"], text="Credit card name"),
                ttk.Label(self.frames_right["credit_cards"], text="Current balance"),
                ttk.Label(self.frames_right["credit_cards"], text="Delete"),
            ]
        )
        for index, title in enumerate(self.titles_credit_cards):
            title.grid(**self.paddings, column=index, row=0, sticky="n")

        self.next_button = ttk.Button(
            self,
            text="Next",
            state="disabled",
        )
        self.next_button.grid(column=0, row=3, columnspan=2, pady=5, padx=5, sticky="ew")

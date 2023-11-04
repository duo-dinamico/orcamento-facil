import tkinter as tk
from tkinter import ttk

from modules.db_crud import (
    create_user,
    login_user,
    create_account,
    read_user_accounts,
    delete_account,
)

from .popups.add_income import AddIncomePopUp
from .popups.add_account import AddAccountPopUp
from .popups.add_credit_card import AddCreditCardPopUp


class StartingPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        # variables
        self.controller = controller
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
        self.information = tk.StringVar()
        self.information.set("Information.")
        self.nome.trace_add("write", self.name_trace)
        self.add_account_button = ttk.Button(
            self.frames_left["adding_details"],
            text="Add account",
            state="disabled",
            command=lambda: self.open_popup(AddAccountPopUp),
        )
        self.add_income_button = ttk.Button(
            self.frames_left["adding_details"],
            text="Add income source",
            state="disabled",
            command=lambda: self.open_popup(AddIncomePopUp),
        )
        self.add_credit_card_button = ttk.Button(
            self.frames_left["adding_details"],
            text="Add credit card",
            state="disabled",
            command=lambda: self.open_popup(AddCreditCardPopUp),
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
                    command=lambda: self.add_user(),
                ),
                ttk.Button(
                    self.frames_left["personal_info"],
                    text="Login",
                    command=lambda: self.login(),
                ),
                ttk.Button(
                    self.frames_left["personal_info"],
                    text="Logout",
                    command=lambda: self.logout(),
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

        ttk.Button(
            self,
            text="Seguinte",
            command=lambda: controller.show_frame("MonthlyCategories"),
        ).grid(column=0, row=3, columnspan=2, pady=5, padx=5, sticky="ew")

        self.refresh_accounts()
        self.refresh_incomes()
        self.refresh_credit_cards()

    def add_user(self):
        state = create_user(self.controller.session, self.nome.get(), self.password.get())
        if state == None:
            self.information.set("User already exists.")
        else:
            self.controller.logged_in = state
            self.information.set(f"Added user: {state}")
            print(self.fields)
            self.fields[1].config(state="disabled")
            self.fields[3].config(state="disabled")
            self.refresh_accounts()

    def login(self):
        state = login_user(self.controller.session, self.nome.get(), self.password.get())
        if state == None:
            self.information.set("Wrong username or password.")
        else:
            self.controller.logged_in = state
            self.information.set(f"Logged in user: {state}")
            self.fields[1].config(state="disabled")
            self.fields[3].config(state="disabled")
            self.refresh_accounts()

    def logout(self):
        self.controller.logged_in = None
        self.information.set(f"Logged in user: {self.controller.logged_in}")
        self.fields[1].config(state="enable")
        self.fields[3].config(state="enable")

    def name_trace(self, *args):
        if self.nome.get() == "":
            self.add_account_button.config(state="disabled")
            self.add_income_button.config(state="disabled")
            self.add_credit_card_button.config(state="disabled")
        else:
            self.add_account_button.config(state="normal")
            self.add_income_button.config(state="normal")
            self.add_credit_card_button.config(state="normal")

    def open_popup(self, popup):
        self.popup = popup(self)

    def add_account(self, account):
        created_id = create_account(
            self.controller.session,
            account["account"],
            self.controller.logged_in,
            account["initial_balance"],
            "BANK",
            account["currency"],
        )
        print(f"add_account: {account}")
        self.accounts.append(account)
        self.popup.destroy()
        self.refresh_accounts()

    def add_income(self, income):
        self.incomes.append(income)
        self.popup.destroy()
        self.refresh_incomes()

    def add_credit_card(self, credit_card):
        self.credit_cards.append(credit_card)
        self.popup.destroy()
        self.refresh_credit_cards()

    def refresh_accounts(self):
        for widget in self.line_widgets:
            widget.destroy()

        # Get the list of accounts
        account_list = read_user_accounts(self.controller.session, self.controller.logged_in)

        if account_list != None:
            for i, item in enumerate(account_list):
                account_label = ttk.Label(self.frames_right["account_list"], text=item.name)
                balance_label = ttk.Label(
                    self.frames_right["account_list"], text=item.initial_balance
                )
                delete_button = ttk.Button(
                    self.frames_right["account_list"],
                    text=item.id,
                    width=4,
                    style="Red.TButton",
                    command=lambda item=item: self.delete_account(item.id),
                )

                account_label.grid(**self.paddings, column=0, row=i + 1, sticky="new")
                balance_label.grid(**self.paddings, column=1, row=i + 1, sticky="new")
                delete_button.grid(**self.paddings, column=2, row=i + 1)

                self.line_widgets.extend([account_label, balance_label, delete_button])

    def refresh_incomes(self):
        for widget in self.line_widgets_incomes:
            widget.destroy()

        for i, item in enumerate(self.incomes):
            income_name_label = ttk.Label(self.frames_right["income_list"], text=item["income"])
            predicted_income_label = ttk.Label(
                self.frames_right["income_list"], text=item["predicted_income"]
            )
            delete_button = ttk.Button(
                self.frames_right["income_list"],
                width=4,
                style="Red.TButton",
                command=lambda i=i: self.delete_income(i),
            )

            income_name_label.grid(**self.paddings, column=0, row=i + 1, sticky="new")
            predicted_income_label.grid(**self.paddings, column=1, row=i + 1, sticky="new")
            delete_button.grid(**self.paddings, column=2, row=i + 1)

            self.line_widgets_incomes.extend(
                [income_name_label, predicted_income_label, delete_button]
            )

    def refresh_credit_cards(self):
        for widget in self.line_widgets_credit_cards:
            widget.destroy()

        for i, item in enumerate(self.credit_cards):
            credit_card_label = ttk.Label(
                self.frames_right["credit_cards"], text=item["credit_card"]
            )
            starting_balance_label = ttk.Label(
                self.frames_right["credit_cards"], text=item["starting_balance"]
            )
            delete_button = ttk.Button(
                self.frames_right["credit_cards"],
                width=4,
                style="Red.TButton",
                command=lambda i=i: self.delete_credit_card(i),
            )

            credit_card_label.grid(**self.paddings, column=0, row=i + 1, sticky="new")
            starting_balance_label.grid(**self.paddings, column=1, row=i + 1, sticky="new")
            delete_button.grid(**self.paddings, column=2, row=i + 1)

            self.line_widgets_credit_cards.extend(
                [credit_card_label, starting_balance_label, delete_button]
            )

    def delete_account(self, account_id):
        delete_account(self.controller.session, account_id, self.controller.logged_in)
        self.refresh_accounts()

    def delete_income(self, income_id):
        del self.incomes[income_id]
        self.refresh_incomes()

    def delete_credit_card(self, card_id):
        del self.credit_cards[card_id]
        self.refresh_credit_cards()

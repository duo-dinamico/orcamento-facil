import tkinter as tk
from tkinter import ttk


class AddAccountPopUp(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.resizable(False, False)
        self.title("Add account")

        self.fields = []
        self.account_name = tk.StringVar()
        self.account_name.trace_add("write", self.activate_add_account)
        self.initial_balance = tk.StringVar()
        self.initial_balance.trace_add("write", self.activate_add_account)
        self.currencies = ["£", "€"]

        frame_popup = ttk.Frame(self)
        frame_popup.pack(anchor="nw", fill="both", expand=True)

        self.fields.append(
            ttk.Label(
                frame_popup,
                text="Account name",
            )
        )
        self.fields.append(ttk.Entry(frame_popup, textvariable=self.account_name))
        self.fields.append(
            ttk.Label(
                frame_popup,
                text="Initial balance",
            )
        )
        self.fields.append(ttk.Entry(frame_popup, textvariable=self.initial_balance))
        self.fields.append(
            ttk.Label(
                frame_popup,
                text="Currency (€ or £)",
            )
        )
        self.currency_combobox = ttk.Combobox(frame_popup, state="readonly", values=self.currencies)
        self.currency_combobox.current(0)
        self.fields.append(self.currency_combobox)

        for field in self.fields:
            field.pack(anchor="w", padx=10, pady=5, fill="x")

        ttk.Button(
            self,
            text="Cancel",
            command=self.cancel_input,
        ).pack(side="left", padx=10, pady=5)
        self.add_account = ttk.Button(
            self,
            text="Add account",
            state="disabled",
            command=lambda: self.parent.add_account(
                {
                    "account": self.account_name.get(),
                    "initial_balance": int(self.initial_balance.get()),
                }
            ),
        )
        self.add_account.pack(side="right", padx=10, pady=5)

    def cancel_input(self):
        self.destroy()

    def activate_add_account(self, *args):
        account_name = self.account_name.get()
        initial_balance = self.initial_balance.get()
        if account_name != "" and initial_balance != 0:
            self.add_account.config(state="enabled")
        else:
            self.add_account.config(state="disabled")


class AddIncomePopUp(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.resizable(False, False)
        self.title("Add income source")

        self.fields = []
        self.income_source_name = tk.StringVar()
        self.income_source_name.trace_add("write", self.activate_add_account)

        frame_popup = ttk.Frame(self)
        frame_popup.pack(anchor="nw", fill="both", expand=True)

        self.fields.append(
            ttk.Label(
                frame_popup,
                text="Income source name",
            )
        )
        self.fields.append(ttk.Entry(frame_popup, textvariable=self.income_source_name))


class StartingPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.fields = []
        self.popup_open = False
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=1)
        self.paddings = {"padx": 10, "pady": 5}
        self.accounts = []
        self.style = ttk.Style()
        self.style.configure("Red.TButton", background="red4", relief="raised")
        self.line_widgets = []
        self.frames_left = {}
        self.frames_right = {}

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
        for index, frame in enumerate(self.frames_left.values()):
            frame.grid(**self.paddings, column=0, row=index, sticky="new")
            frame.rowconfigure(index, weight=1)
        for index, frame in enumerate(self.frames_right.values()):
            frame.grid(**self.paddings, column=1, row=index, sticky="new")
            frame.columnconfigure(0, weight=1)
            frame.columnconfigure(1, weight=1)
            frame.columnconfigure(2, weight=1)

        # Here starts the field listing and building
        self.nome = tk.StringVar()
        self.nome.trace_add("write", self.nome_trace)
        self.fields.append(
            ttk.Label(
                self.frames_left["personal_info"],
                text="Name",
            )
        )
        self.fields.append(ttk.Entry(self.frames_left["personal_info"], textvariable=self.nome))
        self.fields.append(ttk.Label(self.frames_left["personal_info"], text="Password"))
        self.fields.append(ttk.Entry(self.frames_left["personal_info"], show="*"))
        self.fields.append(
            ttk.Button(
                self.frames_left["personal_info"],
                text="Add user",
                command=lambda: self.add_user(),
            )
        )
        self.add_account_button = ttk.Button(
            self.frames_left["adding_details"],
            text="Add account",
            state="disabled",
            command=lambda: self.open_popup(AddAccountPopUp),
        )
        self.fields.append(self.add_account_button)
        self.add_income_button = ttk.Button(
            self.frames_left["adding_details"],
            text="Add income source",
            state="disabled",
            command=lambda: self.open_popup(AddIncomePopUp),
        )
        self.fields.append(self.add_income_button)
        for field in self.fields:
            field.pack(**self.paddings, anchor="w", fill="x")

        self.titles = []
        self.titles.append(ttk.Label(self.frames_right["account_list"], text="Account name"))
        self.titles.append(ttk.Label(self.frames_right["account_list"], text="Initial balance"))
        self.titles.append(ttk.Label(self.frames_right["account_list"], text="Delete"))
        for index, title in enumerate(self.titles):
            title.grid(**self.paddings, column=index, row=0, sticky="new")

        ttk.Button(
            self,
            text="Seguinte",
            command=lambda: controller.show_frame("MonthlyCategories"),
        ).grid(column=0, row=3, columnspan=2, pady=5, padx=5, sticky="ew")

        self.refresh_accounts()

    def add_user(self):
        pass

    def nome_trace(self, *args):
        if self.nome.get() == "":
            self.add_account_button.config(state="disabled")
            self.add_income_button.config(state="disabled")
        else:
            self.add_account_button.config(state="normal")
            self.add_income_button.config(state="normal")

    def open_popup(self, popup):
        if not self.popup_open:
            self.popup = popup(self)
            self.popup_open = True

    def add_account(self, account):
        self.accounts.append(account)
        self.popup.destroy()
        self.popup_open = False
        self.refresh_accounts()

    def refresh_accounts(self):
        for widget in self.line_widgets:
            widget.destroy()

        for i, item in enumerate(self.accounts):
            account_label = ttk.Label(self.frames_right["account_list"], text=item["account"])
            balance_label = ttk.Label(
                self.frames_right["account_list"], text=item["initial_balance"]
            )
            delete_button = ttk.Button(
                self.frames_right["account_list"],
                text="X",
                width=4,
                style="Red.TButton",
                command=lambda i=i: self.delete_account(i),
            )

            account_label.grid(**self.paddings, column=0, row=i + 1, sticky="new")
            balance_label.grid(**self.paddings, column=1, row=i + 1, sticky="new")
            delete_button.grid(**self.paddings, column=2, row=i + 1)

            self.line_widgets.append(account_label)
            self.line_widgets.append(balance_label)
            self.line_widgets.append(delete_button)

    def delete_account(self, index):
        del self.accounts[index]
        self.refresh_accounts()

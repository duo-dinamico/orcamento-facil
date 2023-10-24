import tkinter as tk
from tkinter import ttk


class PopUpWindow(tk.Toplevel):
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
        self.currency = tk.StringVar()
        self.currency.trace_add("write", self.activate_add_account)
        self.style = ttk.Style()
        self.style.configure("White.TEntry", fieldbackground="white")
        self.style.configure("Red.TEntry", fieldbackground="red")

        frame_popup = ttk.Frame(self)
        frame_popup.pack(anchor="nw", fill="both", expand=True)

        self.fields.append(
            ttk.Label(
                master=frame_popup,
                text="Account name",
            )
        )
        self.fields.append(ttk.Entry(master=frame_popup, textvariable=self.account_name))
        self.fields.append(
            ttk.Label(
                master=frame_popup,
                text="Initial balance",
            )
        )
        self.fields.append(ttk.Entry(master=frame_popup, textvariable=self.initial_balance))
        self.fields.append(
            ttk.Label(
                master=frame_popup,
                text="Currency (€ or £)",
            )
        )
        self.currency_entry = ttk.Entry(
            master=frame_popup,
            textvariable=self.currency,
            style="White.TEntry",
        )
        self.fields.append(self.currency_entry)

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

    def check_currency(self, *args):
        accepted_values = ["euro", "pound", "€", "£"]
        current_value = self.currency.get()
        if current_value not in accepted_values:
            self.currency_entry.config(style="Red.TEntry")
        else:
            self.currency_entry.config(style="White.TEntry")

    def activate_add_account(self, *args):
        accepted_values = ["euro", "pound", "€", "£"]
        currency = self.currency.get()
        account_name = self.account_name.get()
        initial_balance = self.initial_balance.get()
        if currency != "" and currency not in accepted_values:
            self.currency_entry.config(style="Red.TEntry")
        elif currency != "" and account_name != "" and initial_balance != 0:
            self.currency_entry.config(style="White.TEntry")
            self.add_account.config(state="enabled")
        else:
            self.add_account.config(state="disabled")
            self.currency_entry.config(style="White.TEntry")


class StartingPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.name = tk.StringVar()
        self.fields = {}
        self.popup_open = False
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.paddings = {"padx": 10, "pady": 5}
        self.accounts = []
        self.accounts_labels = []
        self.buttons = []
        self.style = ttk.Style()
        self.style.configure("Red.TButton", background="red4", relief="raised")

        # Here starts the frame listing and building
        frames_left = {}
        self.frames_right = {}
        frames_left["informacao_pessoal"] = ttk.LabelFrame(
            self, text="Informacao Pessoal", relief="ridge"
        )
        frames_left["adicionar_botoes"] = ttk.LabelFrame(
            self, text="Informacao Adicional", relief="ridge"
        )
        self.frames_right["lista_contas"] = ttk.LabelFrame(
            self, text="Lista de contas", relief="ridge"
        )
        for index, frame in enumerate(frames_left.values()):
            frame.grid(**self.paddings, column=0, row=index, sticky="nsew")
            frame.rowconfigure(index, weight=1)
            frame.columnconfigure(0, weight=1)
        for index, frame in enumerate(self.frames_right.values()):
            frame.grid(**self.paddings, column=1, row=index, sticky="new")
            frame.columnconfigure(0, weight=1)
            frame.columnconfigure(1, weight=1)
            frame.columnconfigure(2, weight=1)

        # Here starts the field listing and building
        self.name.trace_add("write", self.nome_trace)
        self.fields["nome_label"] = ttk.Label(
            master=frames_left["informacao_pessoal"],
            text="Nome",
        )
        self.fields["nome_entry"] = ttk.Entry(
            master=frames_left["informacao_pessoal"], textvariable=self.name
        )
        self.fields["password_label"] = ttk.Label(
            master=frames_left["informacao_pessoal"], text="Password"
        )
        self.fields["password_entry"] = ttk.Entry(
            master=frames_left["informacao_pessoal"], show="*"
        )
        self.fields["add_user_button"] = ttk.Button(
            master=frames_left["informacao_pessoal"],
            text="Add user",
            command=lambda: self.add_user(),
        )
        self.fields["adicionar_conta_button"] = ttk.Button(
            master=frames_left["adicionar_botoes"],
            text="Adicionar conta",
            state="disabled",
            command=self.open_popup,
        )
        self.fields["adicionar_fonte_rendimento_button"] = ttk.Button(
            master=frames_left["adicionar_botoes"],
            text="Adicionar fonte de rendimento",
            state="disabled",
        )
        for field in self.fields.values():
            field.pack(**self.paddings, anchor="w", fill="x")

        self.titles = []
        self.titles.append(ttk.Label(master=self.frames_right["lista_contas"], text="Account name"))
        self.titles.append(
            ttk.Label(master=self.frames_right["lista_contas"], text="Initial balance")
        )
        self.titles.append(ttk.Label(master=self.frames_right["lista_contas"], text="Delete"))
        for index, title in enumerate(self.titles):
            title.grid(**self.paddings, column=index, row=0, sticky="new")

        ttk.Button(
            self,
            text="Seguinte",
            command=lambda: controller.show_frame("MonthlyCategories"),
        ).grid(column=0, row=3, columnspan=2, pady=5, padx=5, sticky="ew")

    def add_user(self):
        pass

    def nome_trace(self, *args):
        if self.name.get() == "":
            self.fields["adicionar_conta_button"].config(state="disabled")
        else:
            self.fields["adicionar_conta_button"].config(state="normal")

    def open_popup(self):
        if not self.popup_open:
            self.popup = PopUpWindow(self)
            self.popup_open = True

    def add_account(self, account):
        self.accounts.append(account)
        self.popup.destroy()
        self.popup_open = False
        self.refresh_accounts()

    def refresh_accounts(self):
        pass

    def place_accounts(self):
        if len(self.accounts_labels) > 0:
            for label in self.accounts_labels:
                label["account"].destroy()
                label["initial_balance"].destroy()
                self.accounts_labels = []
            for button in self.buttons:
                button.destroy()
                self.buttons = []
        for index, account in enumerate(self.accounts):
            self.accounts_labels.append(
                {
                    "account": ttk.Label(
                        master=self.frames_right["lista_contas"], text=account["account"]
                    ),
                    "initial_balance": ttk.Label(
                        master=self.frames_right["lista_contas"], text=account["initial_balance"]
                    ),
                }
            )
            for label in self.accounts_labels:
                label["account"].grid(**self.paddings, column=0, row=index + 1, sticky="new")
                label["initial_balance"].grid(
                    **self.paddings, column=1, row=index + 1, sticky="new"
                )
            self.buttons.append(
                ttk.Button(
                    master=self.frames_right["lista_contas"],
                    text="X",
                    width=4,
                    style="Red.TButton",
                    command=lambda: self.delete_account(index),
                )
            )
            for button in self.buttons:
                button.grid(**self.paddings, column=2, row=index + 1)

    def delete_account(self, index):
        self.accounts.pop(index)
        self.place_accounts()

import tkinter as tk
from tkinter import ttk


class AddIncomePopUp(tk.Toplevel):
    def __init__(self, parent, presenter) -> None:
        super().__init__(master=parent)

        self.transient(parent)
        self.resizable(False, False)
        self.title("Add Income Source")

        self.error_message = tk.StringVar(value="")
        income_name = tk.StringVar()
        expected_income = tk.StringVar()
        real_income = tk.StringVar()
        income_day = tk.StringVar()
        income_month = presenter.get_month()
        recurrence = presenter.get_recurrence()
        target_accounts = presenter.get_target_accounts()

        label_income_name = ttk.Label(self, text="Income source")
        label_income_name.pack(anchor="w", padx=10, pady=5, fill="x")
        entry_income_name = ttk.Entry(self, textvariable=income_name)
        entry_income_name.pack(anchor="w", padx=10, pady=5, fill="x")

        label_target_account = ttk.Label(self, text="Chose target account")
        label_target_account.pack(anchor="w", padx=10, pady=5, fill="x")
        combobox_target_account = ttk.Combobox(self, state="readonly", values=target_accounts)
        combobox_target_account.current(0)
        combobox_target_account.pack(anchor="w", padx=10, pady=5, fill="x")

        label_expected_income = ttk.Label(self, text="Expected income")
        label_expected_income.pack(anchor="w", padx=10, pady=5, fill="x")
        entry_expected_income = ttk.Entry(self, textvariable=expected_income)
        entry_expected_income.pack(anchor="w", padx=10, pady=5, fill="x")

        label_real_income = ttk.Label(self, text="Real income")
        label_real_income.pack(anchor="w", padx=10, pady=5, fill="x")
        entry_real_income = ttk.Entry(self, textvariable=real_income)
        entry_real_income.pack(anchor="w", padx=10, pady=5, fill="x")

        label_income_date = ttk.Label(self, text="Income date")
        label_income_date.pack(anchor="w", padx=10, pady=5, fill="x")
        frame_income_date = ttk.Frame(self)
        frame_income_date.pack(anchor="w", padx=10, pady=5, fill="x")
        entry_income_day = ttk.Entry(frame_income_date, textvariable=income_day)
        entry_income_day.pack(side="left", expand=True, fill="both")
        label_income_day = ttk.Label(frame_income_date, text="/")
        label_income_day.pack(side="left", expand=True, fill="both", padx=10)
        combobox_income_month = ttk.Combobox(frame_income_date, state="readonly", values=income_month)
        combobox_income_month.pack(side="left", expand=True, fill="both")

        label_recurrence = ttk.Label(self, text="Recurrence")
        label_recurrence.pack(anchor="w", padx=10, pady=5, fill="x")
        combobox_recurrence = ttk.Combobox(self, state="readonly", values=recurrence)
        combobox_recurrence.pack(anchor="w", padx=10, pady=5, fill="x")

        label_error_popup = ttk.Label(self, textvariable=self.error_message)
        label_error_popup.pack(anchor="w", padx=10, pady=5, fill="x")

        button_cancel = ttk.Button(self, text="Cancel", command=self.cancel_input)
        button_cancel.pack(side="left", padx=10, pady=5)
        button_add_account = ttk.Button(self, text="Add income source")
        button_add_account.pack(side="right", padx=10, pady=5)
        button_add_account.bind("<Button-1>", presenter.handle_add_income)
        # TODO this should enable us to confirm when we press enter
        # self.bind("<Return>", presenter.handle_add_income)

    def cancel_input(self):
        self.destroy()

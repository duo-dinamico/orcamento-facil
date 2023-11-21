import tkinter as tk
from tkinter import ttk


class AddIncomePopUp(tk.Toplevel):
    def __init__(self, parent, presenter) -> None:
        super().__init__(master=parent)

        self.transient(parent)
        self.resizable(False, False)
        self.title("Add Income Source")

        self.error_message = tk.StringVar(value="")
        self.income_name = tk.StringVar()
        self.expected_income = tk.StringVar()
        self.real_income = tk.StringVar()
        self.income_day = tk.StringVar()
        income_month = presenter.get_month()
        recurrence = presenter.get_recurrence()
        target_accounts = presenter.get_target_accounts()

        lbl_income_name = ttk.Label(self, text="Income source")
        lbl_income_name.pack(anchor="w", padx=10, pady=5, fill="x")
        ent_income_name = ttk.Entry(self, textvariable=self.income_name)
        ent_income_name.pack(anchor="w", padx=10, pady=5, fill="x")

        lbl_target_account = ttk.Label(self, text="Chose target account")
        lbl_target_account.pack(anchor="w", padx=10, pady=5, fill="x")
        self.cbx_target_account = ttk.Combobox(self, state="readonly", values=target_accounts)
        self.cbx_target_account.current(0)
        self.cbx_target_account.pack(anchor="w", padx=10, pady=5, fill="x")

        lbl_expected_income = ttk.Label(self, text="Expected income")
        lbl_expected_income.pack(anchor="w", padx=10, pady=5, fill="x")
        ent_expected_income = ttk.Entry(self, textvariable=self.expected_income)
        ent_expected_income.pack(anchor="w", padx=10, pady=5, fill="x")

        lbl_real_income = ttk.Label(self, text="Real income")
        lbl_real_income.pack(anchor="w", padx=10, pady=5, fill="x")
        ent_real_income = ttk.Entry(self, textvariable=self.real_income)
        ent_real_income.pack(anchor="w", padx=10, pady=5, fill="x")

        lbl_income_date = ttk.Label(self, text="Income date")
        lbl_income_date.pack(anchor="w", padx=10, pady=5, fill="x")
        frm_income_date = ttk.Frame(self)
        frm_income_date.pack(anchor="w", padx=10, pady=5, fill="x")
        ent_income_day = ttk.Entry(frm_income_date, textvariable=self.income_day)
        ent_income_day.pack(side="left", expand=True, fill="both")
        lbl_income_day = ttk.Label(frm_income_date, text="/")
        lbl_income_day.pack(side="left", expand=True, fill="both", padx=10)
        self.cbx_income_month = ttk.Combobox(frm_income_date, state="readonly", values=income_month)
        self.cbx_income_month.pack(side="left", expand=True, fill="both")

        lbl_recurrence = ttk.Label(self, text="Recurrence")
        lbl_recurrence.pack(anchor="w", padx=10, pady=5, fill="x")
        self.cbx_recurrence = ttk.Combobox(self, state="readonly", values=recurrence)
        self.cbx_recurrence.pack(anchor="w", padx=10, pady=5, fill="x")

        lbl_error_popup = ttk.Label(self, textvariable=self.error_message)
        lbl_error_popup.pack(anchor="w", padx=10, pady=5, fill="x")

        btn_cancel = ttk.Button(self, text="Cancel", command=self.cancel_input)
        btn_cancel.pack(side="left", padx=10, pady=5)
        btn_add_income = ttk.Button(self, text="Add income source")
        btn_add_income.pack(side="right", padx=10, pady=5)
        btn_add_income.bind("<Button-1>", presenter.handle_add_income)
        # TODO this should enable us to confirm when we press enter
        # self.bind("<Return>", presenter.handle_add_income)

    def cancel_input(self):
        self.destroy()

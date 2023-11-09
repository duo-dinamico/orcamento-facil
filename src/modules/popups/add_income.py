import tkinter as tk
from tkinter import ttk

from .utils.popup_setup import popup_setup


class AddIncomePopUp(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        popup_setup(self, parent, "Add income source")

        self.fields = []
        self.income_source_name = tk.StringVar()
        self.income_source_name.trace_add("write", self.activate_add_income)
        self.income_source_account_id = tk.StringVar()
        self.predicted_income = tk.StringVar(value="0")
        self.predicted_income.trace_add("write", self.activate_add_income)
        self.income_date_day = tk.StringVar(value="Day")
        self.income_date_month = tk.StringVar(value="Month")
        self.income_frequency_value = tk.IntVar(value=1)
        self.income_frequency = ["Day", "Month", "Year"]

        frame_popup = ttk.Frame(self)
        frame_popup.pack(anchor="nw", fill="both", expand=True)

        self.fields.extend(
            [
                ttk.Label(frame_popup, text="Income source name"),
                ttk.Entry(frame_popup, textvariable=self.income_source_name),
                ttk.Label(frame_popup, text="Account"),
                ttk.Entry(frame_popup, textvariable=self.income_source_account_id),
                ttk.Label(frame_popup, text="Predicted income"),
                ttk.Entry(frame_popup, textvariable=self.predicted_income),
                ttk.Label(frame_popup, text="Income date"),
                ttk.Frame(frame_popup),
            ]
        )

        for field in self.fields:
            field.pack(anchor="w", padx=10, pady=5, fill="x")

        ttk.Entry(self.fields[-1], textvariable=self.income_date_day).pack(
            side="left",
            expand=True,
            fill="both",
        )
        ttk.Entry(self.fields[-1], textvariable=self.income_date_month).pack(
            side="left",
            padx=(10, 10),
            expand=True,
            fill="both",
        )

        ttk.Label(
            frame_popup,
            text="Income frequency",
        ).pack(anchor="w", padx=10, pady=5, fill="x")
        self.frequency_frame = ttk.Frame(self)
        self.frequency_frame.pack(anchor="w", padx=10, pady=5, fill="x")
        ttk.Label(self.frequency_frame, text="Every ").pack(
            side="left",
            expand=True,
            fill="both",
        )
        ttk.Entry(self.frequency_frame, textvariable=self.income_frequency_value).pack(
            side="left",
            padx=(10, 10),
            expand=True,
            fill="both",
        )
        self.frequency_combobox = ttk.Combobox(
            self.frequency_frame, state="readonly", values=self.income_frequency
        )
        self.frequency_combobox.current(1)
        self.frequency_combobox.pack(
            side="left",
            expand=True,
            fill="both",
        )

        ttk.Button(
            self,
            text="Cancel",
            command=self.cancel_input,
        ).pack(side="left", padx=10, pady=5)
        self.add_income = ttk.Button(
            self,
            text="Add income",
            state="disabled",
            command=lambda: self.parent.add_income(
                {
                    "account_id": int(self.income_source_account_id.get()),
                    "name": self.income_source_name.get(),
                    "expected_income_value": int(self.predicted_income.get()),
                    "real_income_value": 0,
                    "income_day": self.income_date_day.get(),
                    "income_month": 1,
                    "recurrency": "ONE",
                }
            ),
        )
        self.add_income.pack(side="right", padx=10, pady=5)

    def cancel_input(self):
        self.destroy()

    def activate_add_income(self, *args):
        income_name = self.income_source_name.get()
        predicted_income = self.predicted_income.get()
        if income_name != "" and int(predicted_income) != 0:
            self.add_income.config(state="enabled")
        else:
            self.add_income.config(state="disabled")

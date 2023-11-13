import tkinter as tk
from tkinter import ttk

from .utils.popup_setup import popup_setup


class AddCreditCardPopUp(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        popup_setup(self, parent, "Add credit card")

        self.fields = []
        self.credit_card_name = tk.StringVar()
        self.credit_card_name.trace_add("write", self.activate_add_credit_card)
        self.starting_balance = tk.StringVar()
        self.starting_balance.trace_add("write", self.activate_add_credit_card)
        self.credit_limit = tk.StringVar()
        self.repayment_date_day = tk.StringVar(value="Day")
        self.interest_rate = tk.StringVar()
        self.instalement_plan = tk.StringVar()

        frame_popup = ttk.Frame(self)
        frame_popup.pack(anchor="nw", fill="both", expand=True)

        self.fields.extend(
            [
                ttk.Label(frame_popup, text="Credit card name"),
                ttk.Entry(frame_popup, textvariable=self.credit_card_name),
                ttk.Label(frame_popup, text="Starting balance"),
                ttk.Entry(frame_popup, textvariable=self.starting_balance),
                ttk.Label(frame_popup, text="Credit limit"),
                ttk.Entry(frame_popup, textvariable=self.credit_limit),
                ttk.Label(frame_popup, text="Repayment day"),
                ttk.Entry(frame_popup, textvariable=self.repayment_date_day),
                ttk.Label(frame_popup, text="Interest rate"),
                ttk.Entry(frame_popup, textvariable=self.interest_rate),
                ttk.Label(frame_popup, text="Plan"),
                ttk.Entry(frame_popup, textvariable=self.instalement_plan),
            ]
        )

        for field in self.fields:
            field.pack(anchor="w", padx=10, pady=5, fill="x")

        ttk.Button(
            self,
            text="Cancel",
            command=self.cancel_input,
        ).pack(side="left", padx=10, pady=5)
        self.add_credit_card = ttk.Button(
            self,
            text="Add credit card",
            state="disabled",
            command=lambda: self.parent.add_credit_card(
                {
                    "credit_card": self.credit_card_name.get(),
                    "starting_balance": int(self.starting_balance.get()),
                }
            ),
        )
        self.add_credit_card.pack(side="right", padx=10, pady=5)

    def cancel_input(self):
        self.destroy()

    def activate_add_credit_card(self, *args):
        credit_card_name = self.credit_card_name.get()
        starting_balance = int(self.starting_balance.get())
        if credit_card_name != "" and starting_balance != 0:
            self.add_credit_card.config(state="enabled")
        else:
            self.add_credit_card.config(state="disabled")

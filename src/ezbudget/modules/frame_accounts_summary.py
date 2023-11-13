from tkinter import ttk


class AccountsSummary(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Account summary")
        label.pack(padx=10, pady=10)

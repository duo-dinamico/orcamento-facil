from tkinter import ttk


categories = {
    "Housing": [{"Mortgage": True}, {"Rent": False}, {"Council Tax": True}],
    "Utilities": [{}],
    "Groceries": [{}],
    "Dining out": [{}],
    "Transportation": [{}],
    "Life essentials": [{}],
    "Fun, Travel and Entertainment": [{}],
    "Subscriptions": [{}],
    "Kids and babies": [{}],
    "Pets": [{}],
}


class MonthlyCategories(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Categorias mensais")
        label.pack(padx=10, pady=10)

        switch_window_button = ttk.Button(
            self,
            text="Next",
            command=lambda: controller.show_frame("AccountsSummary"),
        )
        switch_window_button.pack(side="bottom", fill="x")

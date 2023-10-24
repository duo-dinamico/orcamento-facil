from tkinter import ttk


class MonthlyCategories(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Categorias mensais")
        label.pack(padx=10, pady=10)

        switch_window_button = ttk.Button(
            self,
            text="Go to the Completion Screen",
            command=lambda: controller.show_frame("StartingPage"),
        )
        switch_window_button.pack(side="bottom", fill="x")

import tkinter as tk


class CategoriasMensais(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Categorias mensais")
        label.pack(padx=10, pady=10)

        switch_window_button = tk.Button(
            self,
            text="Go to the Completion Screen",
            command=lambda: controller.show_frame("PaginaInicial"),
        )
        switch_window_button.pack(side="bottom", fill=tk.X)

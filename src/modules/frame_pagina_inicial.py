import tkinter as tk
from tkinter import ttk


class PaginaInicial(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.nome_stringvar = tk.StringVar()
        self.fields = {}

        frames = {}
        frames["informacao_pessoal"] = ttk.LabelFrame(
            self, text="Informacao Pessoal", relief="ridge"
        )
        frames["adicionar_botoes"] = ttk.LabelFrame(
            self, text="Informacao Adicional", relief="ridge"
        )
        for frame in frames.values():
            frame.pack(anchor="w", padx=10, pady=5, expand=True, fill="both")

        self.nome_stringvar.trace_add("write", self.nome_trace)
        self.fields["nome_label"] = ttk.Label(
            master=frames["informacao_pessoal"],
            text="Nome",
        )
        self.fields["nome"] = ttk.Entry(
            master=frames["informacao_pessoal"], textvariable=self.nome_stringvar
        )
        self.fields["password_label"] = ttk.Label(
            master=frames["informacao_pessoal"], text="Password"
        )
        self.fields["password"] = ttk.Entry(master=frames["informacao_pessoal"], show="*")
        self.fields["adicionar_conta"] = ttk.Button(
            master=frames["adicionar_botoes"],
            text="Adicionar conta",
            state="disabled",
        )
        for field in self.fields.values():
            field.pack(anchor="w", padx=10, pady=5, fill="x")

        # We use the switch_window_button in order to call the show_frame() method as a lambda function
        switch_window_button = tk.Button(
            self,
            text="Mudar para categorias mensais",
            command=lambda: controller.show_frame("CategoriasMensais"),
        )
        switch_window_button.pack(side="bottom", fill="x")

    def nome_trace(self, *args):
        if self.nome_stringvar.get() == "":
            self.fields["adicionar_conta"].config(state="disabled")
        else:
            self.fields["adicionar_conta"].config(state="normal")

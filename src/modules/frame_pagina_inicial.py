import tkinter as tk
from tkinter import ttk


class PopUpWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.wm_resizable(False, False)
        self.title("Adicionar conta")
        self.fields = {}

        frame_popup = ttk.Frame(self)
        frame_popup.pack(anchor="nw", fill="both", expand=True)

        self.fields["conta_nome_label"] = ttk.Label(
            master=frame_popup,
            text="Nome conta",
        )
        self.fields["conta_nome_entry"] = ttk.Entry(master=frame_popup)

        for field in self.fields.values():
            field.pack(anchor="w", padx=10, pady=5, fill="x")

    def submit_data(self):
        entered_data = self.data_entry.get()
        print("Entered data:", entered_data)
        self.parent.close_popup()


class PaginaInicial(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.nome_stringvar = tk.StringVar()
        self.fields = {}
        self.popup_open = False

        # Here starts the frame listing and building
        frames = {}
        frames["informacao_pessoal"] = ttk.LabelFrame(
            self, text="Informacao Pessoal", relief="ridge"
        )
        frames["adicionar_botoes"] = ttk.LabelFrame(
            self, text="Informacao Adicional", relief="ridge"
        )
        for frame in frames.values():
            frame.pack(anchor="w", padx=10, pady=5, expand=True, fill="both")

        # Here starts the field listing and building
        self.nome_stringvar.trace_add("write", self.nome_trace)
        self.fields["nome_label"] = ttk.Label(
            master=frames["informacao_pessoal"],
            text="Nome",
        )
        self.fields["nome_entry"] = ttk.Entry(
            master=frames["informacao_pessoal"], textvariable=self.nome_stringvar
        )
        self.fields["password_label"] = ttk.Label(
            master=frames["informacao_pessoal"], text="Password"
        )
        self.fields["password_entry"] = ttk.Entry(master=frames["informacao_pessoal"], show="*")
        self.fields["adicionar_conta_button"] = ttk.Button(
            master=frames["adicionar_botoes"],
            text="Adicionar conta",
            state="disabled",
            command=self.open_popup,
        )
        self.fields["adicionar_fonte_rendimento_button"] = ttk.Button(
            master=frames["adicionar_botoes"],
            text="Adicionar fonte de rendimento",
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
            self.fields["adicionar_conta_button"].config(state="disabled")
        else:
            self.fields["adicionar_conta_button"].config(state="normal")

    def open_popup(self):
        if not self.popup_open:
            self.popup = PopUpWindow(self)
            self.popup_open = True

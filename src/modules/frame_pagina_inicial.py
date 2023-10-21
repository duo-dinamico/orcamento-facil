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
        self.fields["conta_balanco_inicial_label"] = ttk.Label(
            master=frame_popup,
            text="Balanco Inicial",
        )
        self.fields["conta_balanco_inicial_entry"] = ttk.Entry(master=frame_popup)

        for field in self.fields.values():
            field.pack(anchor="w", padx=10, pady=5, fill="x")

        cancel_button = ttk.Button(
            self,
            text="Cancelar",
            command=self.cancel_input,
        )
        cancel_button.pack(side="left", padx=10, pady=5)
        adicionar_button = ttk.Button(
            self,
            text="Adicionar",
            command=self.cancel_input,
        )
        adicionar_button.pack(side="right", padx=10, pady=5)

    def submit_data(self):
        entered_data = self.data_entry.get()
        print("Entered data:", entered_data)
        self.parent.close_popup()

    def cancel_input(self):
        self.destroy()


class PaginaInicial(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.nome_stringvar = tk.StringVar()
        self.fields = {}
        self.popup_open = False
        self.lista_contas = []

        # Here starts the frame listing and building
        top_frame = ttk.Frame(self)
        top_frame.pack(side="top", fill="both", expand=True)
        left_frame = ttk.Frame(top_frame)
        left_frame.pack(side="left", fill="both", expand=True)
        right_frame = ttk.Frame(top_frame)
        right_frame.pack(side="right", fill="both", expand=True)
        frames_left = {}
        frames_right = {}
        frames_left["informacao_pessoal"] = ttk.LabelFrame(
            left_frame, text="Informacao Pessoal", relief="ridge"
        )
        frames_left["adicionar_botoes"] = ttk.LabelFrame(
            left_frame, text="Informacao Adicional", relief="ridge"
        )
        frames_right["lista_contas"] = ttk.LabelFrame(
            right_frame, text="Lista de contas", relief="ridge"
        )
        for frame in frames_left.values():
            frame.pack(padx=10, pady=5, expand=True, fill="both")
        for frame in frames_right.values():
            frame.pack(padx=10, pady=5, expand=True, fill="both")

        # Here starts the field listing and building
        self.nome_stringvar.trace_add("write", self.nome_trace)
        self.fields["nome_label"] = ttk.Label(
            master=frames_left["informacao_pessoal"],
            text="Nome",
        )
        self.fields["nome_entry"] = ttk.Entry(
            master=frames_left["informacao_pessoal"], textvariable=self.nome_stringvar
        )
        self.fields["password_label"] = ttk.Label(
            master=frames_left["informacao_pessoal"], text="Password"
        )
        self.fields["password_entry"] = ttk.Entry(
            master=frames_left["informacao_pessoal"], show="*"
        )
        self.fields["adicionar_conta_button"] = ttk.Button(
            master=frames_left["adicionar_botoes"],
            text="Adicionar conta",
            state="disabled",
            command=self.open_popup,
        )
        self.fields["adicionar_fonte_rendimento_button"] = ttk.Button(
            master=frames_left["adicionar_botoes"],
            text="Adicionar fonte de rendimento",
            state="disabled",
        )
        for field in self.fields.values():
            field.pack(anchor="w", padx=10, pady=5, fill="x")

        ttk.Label(master=frames_right["lista_contas"], text="Nome Conta").pack(
            side="left", anchor="n", padx=10, pady=5, fill="x"
        )
        ttk.Label(master=frames_right["lista_contas"], text="Balanco Inicial").pack(
            side="right", anchor="n", padx=10, pady=5, fill="x"
        )
        # for conta in self.lista_contas:

        # We use the switch_window_button in order to call the show_frame() method as a lambda function
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(side="bottom", fill="both", expand=True)
        ttk.Button(
            bottom_frame,
            text="Seguinte",
            command=lambda: controller.show_frame("CategoriasMensais"),
        ).pack(side="bottom", fill="both", expand=True)

    def nome_trace(self, *args):
        if self.nome_stringvar.get() == "":
            self.fields["adicionar_conta_button"].config(state="disabled")
        else:
            self.fields["adicionar_conta_button"].config(state="normal")

    def open_popup(self):
        if not self.popup_open:
            self.popup = PopUpWindow(self)
            self.popup_open = True

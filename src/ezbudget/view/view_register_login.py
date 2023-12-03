import tkinter as tk

import ttkbootstrap as ttk


class RegisterLogin(ttk.Frame):
    def __init__(self, parent, presenter) -> None:
        super().__init__(master=parent, bootstyle="secondary")
        self.presenter = presenter
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.error_message = tk.StringVar(value="")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)

        frm_login = ttk.Frame(self)
        frm_login.grid(column=1, row=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(frm_login, text="Welcome back!", justify="center", anchor="center", font=("Roboto", 25, "bold")).pack(
            expand=True, fill="x", padx=10, pady=(100, 5)
        )
        ttk.Label(frm_login, text="Please enter your details", justify="center", anchor="center", font=("Roboto")).pack(
            expand=True, fill="x", padx=10, pady=5
        )

        lbl_username = ttk.Label(frm_login, text="Username", font=("Roboto"))
        lbl_username.pack(expand=True, fill="x", padx=10, pady=5)
        ent_username = ttk.Entry(frm_login, textvariable=self.username)
        ent_username.pack(expand=True, fill="x", padx=10, pady=5)

        lbl_password = ttk.Label(frm_login, text="Password", font=("Roboto"))
        lbl_password.pack(expand=True, fill="x", padx=10, pady=5)
        ent_password = ttk.Entry(frm_login, textvariable=self.password, show="*")
        ent_password.pack(expand=True, fill="x", padx=10, pady=5)
        ent_password.bind("<Return>", self.enter_to_login)

        lbl_error = ttk.Label(frm_login, textvariable=self.error_message)
        lbl_error.pack(expand=True, fill="x", padx=10, pady=5)

        btn_login = ttk.Button(frm_login, text="Login", bootstyle="outline")
        btn_login.pack(expand=True, fill="x", padx=10, pady=5)
        btn_login.bind("<Button-1>", self.presenter.handle_login_user)

        btn_register = ttk.Button(frm_login, text="Register")
        btn_register.pack(expand=True, fill="x", padx=10, pady=(5, 100))
        btn_register.bind("<Button-1>", self.presenter.handle_register_user)

    def enter_to_login(self, event):
        del event
        self.presenter.handle_login_user()

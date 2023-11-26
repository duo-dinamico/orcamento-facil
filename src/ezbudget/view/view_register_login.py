import tkinter as tk

import ttkbootstrap as ttk


class RegisterLogin(ttk.Frame):
    def __init__(self, parent, presenter) -> None:
        super().__init__(master=parent)

        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.error_message = tk.StringVar(value="")

        lbl_username = ttk.Label(self, text="Username")
        lbl_username.grid(row=0, column=0, columnspan=2, padx=10, pady=5)
        ent_username = ttk.Entry(self, textvariable=self.username)
        ent_username.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        lbl_password = ttk.Label(self, text="Password")
        lbl_password.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
        ent_password = ttk.Entry(self, textvariable=self.password, show="*")
        ent_password.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        lbl_error = ttk.Label(self, textvariable=self.error_message)
        lbl_error.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        btn_register = ttk.Button(self, text="Register")
        btn_register.grid(row=5, column=0, padx=10, pady=5)
        btn_register.bind("<Button-1>", presenter.handle_register_user)

        btn_login = ttk.Button(self, text="Login")
        btn_login.grid(row=5, column=1, padx=10, pady=5)
        btn_login.bind("<Button-1>", presenter.handle_login_user)

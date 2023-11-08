import tkinter as tk
from tkinter import ttk


class RegisterLogin(tk.Toplevel):
    def __init__(self, parent, presenter) -> None:
        super().__init__(master=parent)

        self.parent = parent
        self.grab_set()
        self.transient(parent)
        self.resizable(False, False)
        self.title("Register or Login")

        self.username_popup = tk.StringVar()
        self.password_popup = tk.StringVar()
        self.error_message = tk.StringVar(value="")

        self.label_username_popup = ttk.Label(self, text="Username")
        self.label_username_popup.grid(row=0, column=0, columnspan=2, padx=10, pady=5)
        self.entry_username_popup = ttk.Entry(self, textvariable=self.username_popup)
        self.entry_username_popup.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
        self.label_password_popup = ttk.Label(self, text="Password")
        self.label_password_popup.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
        self.entry_password_popup = ttk.Entry(self, textvariable=self.password_popup, show="*")
        self.entry_password_popup.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
        self.label_error_popup = ttk.Label(self, textvariable=self.error_message)
        self.label_error_popup.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
        self.button_register_popup = ttk.Button(self, text="Register")
        self.button_register_popup.grid(row=5, column=0, padx=10, pady=5)
        self.button_register_popup.bind("<Button-1>", presenter.handle_register_user)
        self.button_login_popup = ttk.Button(self, text="Login")
        self.button_login_popup.grid(row=5, column=1, padx=10, pady=5)
        self.button_login_popup.bind("<Button-1>", parent.show_starting_view)

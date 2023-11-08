import tkinter as tk
from tkinter import ttk
from typing import Protocol

from . import RegisterLogin
from .starting_view import StartingView

TITLE = "Ez Budget"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800


class Presenter(Protocol):
    def handle_register_user(self, event=None):
        ...


class RootView(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(TITLE)
        self.resizable(False, False)

        # Put the windows in the center of the screen
        x_center = self.winfo_screenwidth() / 2 - WINDOW_WIDTH / 2
        y_center = self.winfo_screenheight() / 2 - WINDOW_HEIGHT / 2
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{int(x_center)}+{int(y_center)}")

    def init_ui(self, presenter: Presenter) -> None:
        self.frame = ttk.Frame(self)
        self.frame.grid(column=0, row=0, sticky="nsew")

        self.register_login_popup = RegisterLogin(self, presenter)
        self.starting_view = StartingView(self)

        self.current_frame = None
        self.current_popup = None

        self.show_register_login_popup()

    def user_created(self):
        self.current_popup.error_message.set("User has been created")

    def show_register_login_popup(self):
        if self.current_popup:
            self.current_popup.destroy()
        self.current_popup = self.register_login_popup

    def show_starting_view(self, event=None):
        if self.current_popup:
            self.current_popup.destroy()
        self.current_frame = self.starting_view
        self.current_frame.grid(column=0, row=0, sticky="nsew")

    def show_temp_view(self, event=None):
        if self.current_popup:
            self.current_popup.destroy()
        self.current_frame = StartingPage(self.frame, self)
        self.current_frame.grid(column=0, row=0, sticky="nsew")

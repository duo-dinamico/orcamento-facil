import tkinter as tk
from typing import Protocol

from . import RegisterLogin
from .starting_view import StartingView

TITLE = "Ez Budget"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800


class Presenter(Protocol):
    def handle_register_user(self, event=None):
        ...

    def run(self) -> None:
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
        self.register_login_popup = RegisterLogin(self, presenter)
        self.starting_view = StartingView(self)

        self.current_frame = None
        self.current_popup = None

        self.show_register_login_popup()

    def error_message_set(self, message: str) -> None:
        self.current_popup.error_message.set(message)

    def get_username_and_password(self) -> {str, str}:
        return {
            "username": self.current_popup.username_popup.get(),
            "password": self.current_popup.password_popup.get(),
        }

    def show_register_login_popup(self) -> None:
        if self.current_popup:
            self.current_popup.destroy()
        self.current_popup = self.register_login_popup

    def show_starting_view(self, event=None) -> None:
        if self.current_popup:
            self.current_popup.destroy()
        self.current_frame = self.starting_view
        self.current_frame.pack(expand=True, fill="both")

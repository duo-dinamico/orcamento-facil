from __future__ import annotations

from typing import Protocol

from model import Model


class View(Protocol):
    def user_created(self) -> None:
        ...


class Presenter:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view

    def handle_register_user(self, event=None) -> None:
        self.model.add_user()
        self.view.user_created()

    def run(self) -> None:
        self.view.init_ui(self)
        self.view.mainloop()

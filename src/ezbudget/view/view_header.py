import ttkbootstrap as ttk


class Header(ttk.Frame):
    def __init__(self, parent, presenter) -> None:
        super().__init__(master=parent)
        self.presenter = presenter

        username = self.set_username()

        lbl_header = ttk.Label(self, text=f" Hello {username}!", font=("Roboto", 14, "bold"))
        lbl_header.pack(fill="x", expand=True, side="left")
        btn_header = ttk.Button(self, text="Settings")
        btn_header.pack(side="left", padx=(0, 10))

    def set_username(self):
        return self.presenter.handle_set_username()

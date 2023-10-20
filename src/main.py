import tkinter as tk
from tkinter import ttk


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Constants
        WINDOW_WIDTH = 1200
        WINDOW_HEIGHT = 800

        self.wm_title("Orçamento Fácil")

        self.wm_resizable(False, False)  # Prevent resizing ???
        x_center = self.winfo_screenwidth() / 2 - WINDOW_WIDTH / 2
        y_center = self.winfo_screenheight() / 2 - WINDOW_HEIGHT / 2
        self.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{int(x_center)}+{int(y_center)}"
        )  # Put the windows in the center of the screen

        message = ttk.Label(self, text="Hello, World!")
        message.pack()


if __name__ == "__main__":
    root = MainWindow()
    root.mainloop()

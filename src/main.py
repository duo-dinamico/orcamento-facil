from tkinter import *
from tkinter import ttk


class MainWindow:
    def __init__(self, root):
        # Constants
        WINDOW_WIDTH = 1200
        WINDOW_HEIGHT = 800

        root.title("Orçamento Fácil")

        root.resizable(False, False)  # Prevent resizing ???
        x_center = root.winfo_screenwidth() / 2 - WINDOW_WIDTH / 2
        y_center = root.winfo_screenheight() / 2 - WINDOW_HEIGHT / 2
        root.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{int(x_center)}+{int(y_center)}"
        )  # Put the windows in the center of the screen

        message = ttk.Label(root, text="Hello, World!")
        message.pack()


if __name__ == "__main__":
    root = Tk()
    MainWindow(root)
    root.mainloop()

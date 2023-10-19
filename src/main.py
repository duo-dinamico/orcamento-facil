#!/usr/bin/env python
import tkinter as tk


def get_horizontal_center():
    x_center = root.winfo_screenwidth() / 2 - WINDOW_WIDTH / 2
    y_center = root.winfo_screenheight() / 2 - WINDOW_HEIGHT / 2
    return f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{int(x_center)}+{int(y_center)}"


if __name__ == "__main__":
    # Constants
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800

    # Start the window
    root = tk.Tk()
    root.title("Orçamento Fácil")  # Name of the window
    root.resizable(False, False)  # Prevent resizing ???
    root.geometry(f"{get_horizontal_center()}")  # Put the windows in the center of the screen

    message = tk.Label(root, text="Hello, World!")
    message.pack()
    root.mainloop()

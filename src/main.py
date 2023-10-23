import tkinter as tk
from tkinter import ttk

from modules.frame_pagina_inicial import PaginaInicial
from modules.frame_categorias_mensais import CategoriasMensais

from db.database import SessionLocal, engine
from db.models import Base


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
        self.wm_geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{int(x_center)}+{int(y_center)}"
        )  # Put the windows in the center of the screen

        # creating a frame and assigning it to container
        container = ttk.Frame(self, height=WINDOW_HEIGHT, width=WINDOW_WIDTH)
        # specifying the region where the frame is packed in root
        container.pack(anchor="nw", fill="both", expand=True)

        # configuring the location of the container using grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # We will now create a dictionary of frames
        self.frames = {}
        # we'll create the frames themselves later but let's add the components to the dictionary.
        for F in (PaginaInicial, CategoriasMensais):
            frame = F(container, self)

            # the windows class acts as the root window for the frames.
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Using a method to switch frames
        self.show_frame("PaginaInicial")

    def show_frame(self, cont):
        frame = self.frames[cont]
        # raises the current frame to the top
        frame.tkraise()


if __name__ == "__main__":
    # Start database
    Base.metadata.create_all(engine)
    db = SessionLocal()

    root = MainWindow()
    root.mainloop()

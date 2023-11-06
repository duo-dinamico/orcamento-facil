import tkinter as tk
from tkinter import ttk

from modules.frame_starting_page import StartingPage
from modules.frame_monthly_categories import MonthlyCategories
from modules.frame_accounts_summary import AccountsSummary

from modules.db_database import SessionLocal, engine
from modules.db_models import Base
from modules.utils.logging import logger


class MainWindow(tk.Tk):
    def __init__(self, session, logged_in, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        logger.info("---Start of the API.---")

        # Pass the db session
        self.session = session
        self.logged_in = logged_in

        # Constants
        window_width = 1200
        window_height = 800

        self.wm_title("Ez Budget")

        self.resizable(False, False)  # Prevent resizing
        x_center = self.winfo_screenwidth() / 2 - window_width / 2
        y_center = self.winfo_screenheight() / 2 - window_height / 2
        self.wm_geometry(
            f"{window_width}x{window_height}+{int(x_center)}+{int(y_center)}"
        )  # Put the windows in the center of the screen
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        container = ttk.Frame(self)  # creating a frame and assigning it to container
        container.grid(column=0, row=0, sticky="nsew")
        # configuring the location of the container using grid
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}  # We will now create a dictionary of frames
        for F in (
            StartingPage,
            MonthlyCategories,
            AccountsSummary,
        ):  # add the components to the dictionary.
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartingPage")  # Using a method to switch frames

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


if __name__ == "__main__":
    Base.metadata.create_all(engine)  # Start database
    session = SessionLocal()
    logged_in = None

    root = MainWindow(session, logged_in=None)
    root.mainloop()

# from modules.db_database import SessionLocal, engine
# from modules.db_models import Base
# from modules.utils.logging import logger

from view import RootView
from presenter import Presenter
from model import Model


def main() -> None:
    model = Model()
    view = RootView()
    presenter = Presenter(model, view)
    presenter.run()

    # def __init__(self) -> None:
    #     super().__init__()

    # logger.info("---Start of the API.---")

    # Pass the db session
    # self.session = session
    # self.logged_in = logged_in

    # configuring the location of the container using grid
    # container.rowconfigure(0, weight=1)
    # container.columnconfigure(0, weight=1)

    # self.frames = {}  # We will now create a dictionary of frames
    # for F in (
    #     StartingPage,
    #     MonthlyCategories,
    #     AccountsSummary,
    #     RegisterLogin,
    # ):  # add the components to the dictionary.
    #     frame = F(container, self)
    #     self.frames[F.__name__] = frame
    #     frame.grid(row=0, column=0, sticky="nsew")

    # self.show_frame("RegisterLogin")  # Using a method to switch frames

    # def show_frame(self, cont):
    #     frame = self.frames[cont]
    #     frame.tkraise()


if __name__ == "__main__":
    main()
    # Base.metadata.create_all(engine)  # Start database
    # session = SessionLocal()
    # logged_in = None

    # root = MainWindow(session, logged_in=None)
    # root.mainloop()

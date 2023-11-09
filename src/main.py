# from modules.db_database import SessionLocal, engine
# from modules.db_models import Base
# from modules.utils.logging import logger

from view import RootView
from presenter import Presenter
from model import Model
from modules.db.db_models import Base
from modules.utils.logging import logger


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


if __name__ == "__main__":
    main()

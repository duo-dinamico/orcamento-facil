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

    # logger.info("---Start of the API.---")


if __name__ == "__main__":
    main()

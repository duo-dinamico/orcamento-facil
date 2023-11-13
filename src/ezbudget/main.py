from presenter import Presenter

from .model import Model
from .view import RootView


def main() -> None:
    model = Model()
    view = RootView()
    presenter = Presenter(model, view)
    presenter.run()


if __name__ == "__main__":
    main()

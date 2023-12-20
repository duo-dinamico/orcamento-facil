from ezbudget.model import Model
from ezbudget.presenter import Presenter
from ezbudget.view import RootView


def main() -> None:
    model = Model()
    view = RootView()
    presenter = Presenter(model, view)
    presenter.run()


if __name__ == "__main__":
    main()

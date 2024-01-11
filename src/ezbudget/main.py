import sys

from PySide6.QtWidgets import QApplication

from ezbudget.model import Model
from ezbudget.presenter import Presenter
from ezbudget.view import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    model = Model()
    presenter = Presenter(model, None)
    view = MainWindow(presenter)
    presenter.view = view

    view.show()

    app.exec()


if __name__ == "__main__":
    main()

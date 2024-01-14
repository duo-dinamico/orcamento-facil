import os
import sys
import tomllib

from PySide6.QtWidgets import QApplication

from ezbudget.model import Model
from ezbudget.presenter import Presenter
from ezbudget.view import MainWindow

basedir = os.path.dirname(__file__)


def main() -> None:
    with open(f"{basedir}/categories_data.toml", mode="rb") as doc:
        category_data = tomllib.load(doc)

    app = QApplication(sys.argv)
    model = Model(category_data)
    presenter = Presenter(model, None)
    view = MainWindow(presenter)
    presenter.view = view

    view.show()

    app.exec()


if __name__ == "__main__":
    main()

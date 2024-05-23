import os
import sys
import tomllib

import qdarkstyle
from PySide6.QtWidgets import QApplication

from ezbudget.model import Model
from ezbudget.presenter import Presenter
from ezbudget.view import MainWindow

BASEDIR = os.path.dirname(__file__)


def main() -> None:
    with open(f"{BASEDIR}/categories_data.toml", mode="rb") as doc:
        category_data = tomllib.load(doc)

    with open(f"{BASEDIR}/currencies.toml", mode="rb") as doc:
        currency_data = tomllib.load(doc)

    app = QApplication(sys.argv)
    # setup stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())
    model = Model(category_data, currency_data)
    presenter = Presenter(model)
    view = MainWindow(presenter, BASEDIR)
    presenter.view = view

    view.show()

    app.exec()


if __name__ == "__main__":
    main()

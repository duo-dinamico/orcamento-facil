from PySide6 import QtGui
from PySide6.QtWidgets import QMainWindow, QStackedWidget

from ezbudget.view import HomePageView, LoginView, SettingsView

TITLE = "Ez Budget"
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768


class MainWindow(QMainWindow):
    def __init__(self, presenter, basedir):
        super().__init__()

        self.presenter = presenter
        self.basedir = basedir

        # setup the window
        self.setWindowTitle(TITLE)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.center()

        self.stacked_widget = QStackedWidget()

        self.login_view = LoginView(self.presenter)

        self.stacked_widget.addWidget(self.login_view)

        self.stacked_widget.setCurrentIndex(0)

        self.setCentralWidget(self.stacked_widget)

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def show_homepage(self, user):
        self.homepage_view = HomePageView(self.presenter, user)
        self.stacked_widget.addWidget(self.homepage_view)
        self.stacked_widget.setCurrentIndex(1)

    def show_settings(self, user):
        self.settings_view = SettingsView(self.presenter, self.basedir, user)
        self.stacked_widget.addWidget(self.settings_view)
        self.stacked_widget.setCurrentIndex(2)

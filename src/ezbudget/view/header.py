from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget


class HeaderView(QWidget):
    def __init__(self, presenter, user):
        super().__init__()
        self.presenter = presenter

        # guiding style
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("white"))
        self.setPalette(palette)

        # setup the layout
        hbl_header = QHBoxLayout()
        hbl_header.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # label for the user
        self.lbl_header_user = QLabel(f"Hello {user.username}!")
        btn_settings = QPushButton("Settings")
        btn_settings.clicked.connect(self.presenter.open_settings_view)

        hbl_header.addWidget(self.lbl_header_user)
        hbl_header.addWidget(btn_settings)

        # set the base layout
        self.setLayout(hbl_header)

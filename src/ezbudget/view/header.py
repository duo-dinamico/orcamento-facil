from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget


class HeaderView(QWidget):
    def __init__(self, user):
        super().__init__()

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
        hbl_header.addWidget(self.lbl_header_user)

        # set the base layout
        self.setLayout(hbl_header)

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
)

from ezbudget.view.styles import MainTitle


class LoginView(QWidget):
    def __init__(self, presenter):
        super().__init__()
        self.presenter = presenter

        # widgets
        hbl_base_layout = QHBoxLayout()
        frm_layout = QFormLayout()
        self.lbl_error_message = QLabel("")
        self.lne_password = QLineEdit()
        self.lne_username = QLineEdit()
        btn_login = QPushButton("Login")
        btn_register = QPushButton("Register")

        lbl_welcome = MainTitle("Welcome!")

        # layout configuration
        hbl_base_layout.insertStretch(0, 2)
        hbl_base_layout.addLayout(frm_layout, 1)
        frm_layout.setFormAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignCenter)

        # form entries
        self.lne_password.setEchoMode(QLineEdit.Password)
        self.lne_password.setPlaceholderText("Enter password...")
        self.lne_username.setPlaceholderText("Enter username...")
        frm_layout.addRow(lbl_welcome)
        frm_layout.addRow("Username:", self.lne_username)
        frm_layout.addRow("Password:", self.lne_password)
        self.lne_password.returnPressed.connect(lambda: self.presenter.login(self.get_user_data()))

        # error message
        frm_layout.addRow(self.lbl_error_message)
        self.lbl_error_message.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignCenter)

        # buttons
        frm_layout.addRow(btn_login)
        frm_layout.addRow(btn_register)
        btn_login.clicked.connect(lambda: self.presenter.login(self.get_user_data()))
        btn_register.clicked.connect(lambda: self.presenter.register(self.get_user_data()))

        # set the base layout
        self.setLayout(hbl_base_layout)

    def get_user_data(self):
        return {"username": self.lne_username.text(), "password": self.lne_password.text()}

    def set_error(self, message):
        self.lbl_error_message.setText(message)

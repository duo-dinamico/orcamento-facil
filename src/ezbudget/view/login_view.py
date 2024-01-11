from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
)


class LoginView(QWidget):
    def __init__(self, presenter):
        super().__init__()
        self.presenter = presenter

        # welcome label
        lbl_welcome = QLabel("Welcome!")
        fnt_welcome = lbl_welcome.font()
        fnt_welcome.setPointSize(30)
        lbl_welcome.setFont(fnt_welcome)
        lbl_welcome.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        # layout configuration
        hbl_base_layout = QHBoxLayout()
        frm_layout = QFormLayout()
        hbl_base_layout.insertStretch(0, 2)
        hbl_base_layout.addLayout(frm_layout, 1)
        frm_layout.setFormAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignCenter)

        # form entries
        self.ent_password = QLineEdit()
        self.ent_password.setEchoMode(QLineEdit.Password)
        self.ent_username = QLineEdit()
        frm_layout.addRow(lbl_welcome)
        frm_layout.addRow("Username:", self.ent_username)
        frm_layout.addRow("Password:", self.ent_password)
        self.ent_password.returnPressed.connect(lambda: self.presenter.login(self.get_user_data()))

        # error message
        self.lbl_error_message = QLabel("")
        frm_layout.addRow(self.lbl_error_message)
        self.lbl_error_message.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignCenter)

        # buttons
        btn_login = QPushButton("Login")
        btn_register = QPushButton("Register")
        frm_layout.addRow(btn_login)
        frm_layout.addRow(btn_register)
        btn_login.clicked.connect(lambda: self.presenter.login(self.get_user_data()))
        btn_register.clicked.connect(lambda: self.presenter.register(self.get_user_data()))

        # set the base layout
        self.setLayout(hbl_base_layout)

    def get_user_data(self):
        return {"username": self.ent_username.text(), "password": self.ent_password.text()}

    def set_error(self, message):
        self.lbl_error_message.setText(message)

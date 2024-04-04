import toml
from cryptography.fernet import Fernet
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ezbudget.view.styles import MainTitle

USER_SETTINGS_FILETYPE = "toml"


class SettingsView(QWidget):
    def __init__(self, presenter, basedir, user):
        super().__init__()
        self.presenter = presenter
        self.basedir = basedir
        self.checkboxes = {}
        self.user_settings = {"default_currency": None, "user_currencies": []}
        self.settings_filename = f"{user.username}_settings"
        self.cipher_suite = Fernet(user.personal_key)

        # layout widgets
        vbl_main_layout = QVBoxLayout()
        hbl_buttons = QHBoxLayout()
        hbl_group_settings = QHBoxLayout()
        self.frm_settings = QFormLayout()

        # group boxes
        grb_currencies = QGroupBox("Currencies")

        # other widgets
        btn_save = QPushButton("Save")
        btn_close = QPushButton("Close")
        self.cbx_currencies = QComboBox()

        # custom widgets
        lbl_main_title = MainTitle("Settings")

        # signal setup
        btn_close.clicked.connect(self.presenter.close_settings_view)
        btn_save.clicked.connect(self.save_settings)
        self.cbx_currencies.currentTextChanged.connect(self.get_user_settings)

        # populate data
        self.populate_currencies()

        # setup the form and group boxes
        self.frm_settings.addRow("Default currency", self.cbx_currencies)
        self.frm_settings.addWidget(QLabel("Select needed currencies:"))
        self.populate_currency_checkboxes()
        grb_currencies.setLayout(self.frm_settings)

        # setup the buttons
        hbl_buttons.addWidget(btn_save)
        hbl_buttons.addWidget(btn_close)

        # setup the main layout
        hbl_group_settings.addWidget(grb_currencies)
        vbl_main_layout.addWidget(lbl_main_title)
        vbl_main_layout.addLayout(hbl_group_settings)
        vbl_main_layout.addLayout(hbl_buttons)

        self.read_saved_setting()

        # set the main layout
        self.setLayout(vbl_main_layout)

    def get_user_settings(self, widget_return: str | int):
        if isinstance(widget_return, str):
            self.user_settings["default_currency"] = widget_return
        if isinstance(widget_return, int):
            self.user_settings["user_currencies"].clear()
            for currency_name, checkbox in self.checkboxes.items():
                if checkbox.isChecked():
                    self.user_settings["user_currencies"].append(currency_name)
        return self.user_settings

    def save_settings(self):
        encrypted_settings = self.cipher_suite.encrypt(toml.dumps(self.user_settings).encode())
        with open(f"{self.basedir}/{self.settings_filename}.{USER_SETTINGS_FILETYPE}", "wb") as file:
            file.write(encrypted_settings)

        self.presenter.close_settings_view()

    def populate_currencies(self):
        currencies = self.presenter.get_currency()
        for currency in currencies:
            self.cbx_currencies.addItem(currency.name)

    def populate_currency_checkboxes(self):
        currencies = self.presenter.get_currency()
        for currency in currencies:
            checkbox = QCheckBox()
            self.checkboxes[currency.name] = checkbox
            self.frm_settings.addRow(currency.name, checkbox)
            checkbox.stateChanged.connect(self.get_user_settings)

    def read_saved_setting(self):
        try:
            with open(f"{self.basedir}/{self.settings_filename}.{USER_SETTINGS_FILETYPE}", "rb") as file:
                encrypted_settings = file.read()
            if encrypted_settings is not None:
                decrypted_settings = toml.loads(self.cipher_suite.decrypt(encrypted_settings).decode())
                self.cbx_currencies.setCurrentText(decrypted_settings["default_currency"])
                for currency_name, checkbox in self.checkboxes.items():
                    if currency_name in decrypted_settings["user_currencies"]:
                        checkbox.setChecked(True)
        except FileNotFoundError:
            with open(f"{self.basedir}/{self.settings_filename}.{USER_SETTINGS_FILETYPE}", "wb") as file:
                pass

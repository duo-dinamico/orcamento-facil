from PySide6.QtCore import QAbstractTableModel, QDate, QModelIndex, Qt, QTimer
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QDateEdit,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)


class TableModel(QAbstractTableModel):
    def __init__(self, accounts, headers):
        super().__init__()
        self.accounts = accounts
        self.headers = headers

    def rowCount(self, parent=QModelIndex()):
        return len(self.accounts)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(self.accounts[index.row()][index.column()])

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]


class IncomingOutgoing(QWidget):
    def __init__(self, presenter):
        super().__init__()
        self.presenter = presenter

        # instances of necessary widgets
        hbl_incoming_outgoing = QHBoxLayout()
        hbl_accounts_controls = QHBoxLayout()
        hbl_incomings_controls = QHBoxLayout()
        hbl_credit_cards_controls = QHBoxLayout()
        vbl_accounts = QVBoxLayout()
        vbl_incomings = QVBoxLayout()
        vbl_credit_cards = QVBoxLayout()
        vbl_accounts_controls = QVBoxLayout()
        vbl_incomings_controls = QVBoxLayout()
        vbl_credit_cards_controls = QVBoxLayout()
        frm_add_edit_accounts = QFormLayout()
        frm_add_edit_incomings = QFormLayout()
        frm_add_edit_credit_cards = QFormLayout()
        grb_accounts_controls = QGroupBox("Manage accounts")
        grb_incomings_controls = QGroupBox("Manage income sources")
        grb_credit_cards_controls = QGroupBox("Manage credit cards")
        self.lne_account_name = QLineEdit()
        self.lne_incoming_name = QLineEdit()
        self.lne_incoming_real = QLineEdit()
        self.lne_credit_card_name = QLineEdit()
        self.cbx_account_currency = QComboBox()
        self.cbx_incoming_account = QComboBox()
        self.cbx_incoming_currency = QComboBox()
        self.cbx_incoming_recurrence = QComboBox()
        self.cbx_incoming_recurrent = QComboBox()
        self.cbx_credit_card_currency = QComboBox()
        self.lbl_account_error_message = QLabel("")
        self.lbl_income_error_message = QLabel("")
        self.lbl_credit_card_error_message = QLabel("")
        lbl_accounts_title = QLabel("Cash & Bank Accounts")
        lbl_incomes_title = QLabel("Income sources")
        lbl_credit_cards_title = QLabel("Credit cards")
        lbl_account_mandatory_fields = QLabel("Fields with an asterisk (*) are mandatory")
        lbl_income_mandatory_fields = QLabel("Fields with an asterisk (*) are mandatory")
        lbl_credit_card_mandatory_fields = QLabel("Fields with an asterisk (*) are mandatory")
        self.dte_incoming_date = QDateEdit()
        btn_account_add = QPushButton("Add account")
        btn_account_edit = QPushButton("Edit account")
        btn_account_delete = QPushButton("Delete account")
        self.btn_incoming_add = QPushButton("Add income source")
        btn_incoming_edit = QPushButton("Edit income source")
        btn_incoming_delete = QPushButton("Delete incoime source")
        btn_credit_card_add = QPushButton("Add credit card")
        btn_credit_card_edit = QPushButton("Edit credit card")
        btn_credit_card_delete = QPushButton("Delete credit card")
        self.tbl_accounts = QTableView()
        self.tbl_incomings = QTableView()
        self.tbl_credit_cards = QTableView()
        self.dsp_account_balance = QDoubleSpinBox()
        self.dsp_incoming_expected = QDoubleSpinBox()
        self.dsp_credit_card_balance = QDoubleSpinBox()
        self.dsp_credit_card_limit = QDoubleSpinBox()

        # setup of calendar
        min_date = QDate(QDate.currentDate().year(), 1, 1)
        max_date = QDate(QDate.currentDate().year(), 12, 31)
        self.dte_incoming_date.setCalendarPopup(True)
        self.dte_incoming_date.setDisplayFormat("dd/MM")
        self.dte_incoming_date.setDate(QDate.currentDate())
        self.dte_incoming_date.setDateRange(min_date, max_date)
        self.dte_incoming_date.setAlignment(Qt.AlignmentFlag.AlignRight)

        # setup combobox and buttons
        self.populate_currencies()
        self.populate_target_accounts()
        self.populate_recurrence()
        btn_account_edit.setEnabled(False)
        btn_account_delete.setEnabled(False)
        btn_account_add.clicked.connect(lambda: self.presenter.create_account(self.get_account_data(), "BANK"))
        self.btn_incoming_add.setEnabled(False)
        btn_incoming_edit.setEnabled(False)
        btn_incoming_delete.setEnabled(False)
        self.btn_incoming_add.clicked.connect(lambda: self.presenter.create_income(self.get_income_source_data()))
        btn_credit_card_edit.setEnabled(False)
        btn_credit_card_delete.setEnabled(False)
        btn_credit_card_add.clicked.connect(lambda: self.presenter.create_account(self.get_credit_card_data(), "CARD"))

        # organize the buttons into the controls layout
        hbl_accounts_controls.addWidget(btn_account_add)
        hbl_accounts_controls.addWidget(btn_account_edit)
        hbl_accounts_controls.addWidget(btn_account_delete)
        hbl_incomings_controls.addWidget(self.btn_incoming_add)
        hbl_incomings_controls.addWidget(btn_incoming_edit)
        hbl_incomings_controls.addWidget(btn_incoming_delete)
        hbl_credit_cards_controls.addWidget(btn_credit_card_add)
        hbl_credit_cards_controls.addWidget(btn_credit_card_edit)
        hbl_credit_cards_controls.addWidget(btn_credit_card_delete)

        # configure entries
        self.lne_account_name.setPlaceholderText("Enter account name...")
        self.dsp_account_balance.setMaximum(999999.99)
        self.dsp_account_balance.setMinimum(-999999.99)
        self.dsp_account_balance.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.cbx_account_currency.currentTextChanged.connect(self.on_account_currency_change)
        self.on_account_currency_change()
        self.lne_incoming_name.setPlaceholderText("Enter income name...")
        self.dsp_incoming_expected.setMaximum(999999.99)
        self.dsp_incoming_expected.setMinimum(-999999.99)
        self.dsp_incoming_expected.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.cbx_incoming_currency.currentTextChanged.connect(self.on_income_currency_change)
        self.on_income_currency_change()
        self.lne_credit_card_name.setPlaceholderText("Enter card name...")
        self.dsp_credit_card_balance.setMaximum(999999.99)
        self.dsp_credit_card_balance.setMinimum(-999999.99)
        self.dsp_credit_card_limit.setMaximum(999999.99)
        self.dsp_credit_card_limit.setMinimum(-999999.99)
        self.dsp_credit_card_balance.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.dsp_credit_card_limit.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.cbx_credit_card_currency.currentTextChanged.connect(self.on_credit_card_currency_change)
        self.on_credit_card_currency_change()

        # add the entries into the form layout
        frm_add_edit_accounts.addRow("Name (*)", self.lne_account_name)
        frm_add_edit_accounts.addRow("Currency (*)", self.cbx_account_currency)
        frm_add_edit_accounts.addRow("Balance", self.dsp_account_balance)

        frm_add_edit_incomings.addRow("Name (*)", self.lne_incoming_name)
        frm_add_edit_incomings.addRow("Account (*)", self.cbx_incoming_account)
        frm_add_edit_incomings.addRow("Currency (*)", self.cbx_incoming_currency)
        frm_add_edit_incomings.addRow("Expected income", self.dsp_incoming_expected)
        frm_add_edit_incomings.addRow("Expected date", self.dte_incoming_date)
        self.cbx_incoming_recurrent.addItems(["Yes", "No"])
        frm_add_edit_incomings.addRow("Recurrent", self.cbx_incoming_recurrent)
        self.cbx_incoming_recurrent.currentIndexChanged.connect(self.on_recurrent_change)
        frm_add_edit_incomings.addRow("Recurrence", self.cbx_incoming_recurrence)

        frm_add_edit_credit_cards.addRow("Name (*)", self.lne_credit_card_name)
        frm_add_edit_credit_cards.addRow("Balance (*)", self.dsp_credit_card_balance)
        frm_add_edit_credit_cards.addRow("Currency", self.cbx_credit_card_currency)
        frm_add_edit_credit_cards.addRow("Credit limit", self.dsp_credit_card_limit)

        # setup the tables
        self.tbl_accounts.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tbl_accounts.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tbl_accounts.clicked.connect(self.on_account_table_view_selection)
        accounts_header = self.tbl_accounts.horizontalHeader()
        accounts_header.setSectionResizeMode(QHeaderView.Stretch)
        self.tbl_incomings.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tbl_incomings.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tbl_incomings.clicked.connect(self.on_incoming_table_view_selection)
        incomings_header = self.tbl_incomings.horizontalHeader()
        incomings_header.setSectionResizeMode(QHeaderView.Stretch)
        self.tbl_credit_cards.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tbl_credit_cards.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tbl_credit_cards.clicked.connect(self.on_credit_card_table_view_selection)
        credit_cards_header = self.tbl_credit_cards.horizontalHeader()
        credit_cards_header.setSectionResizeMode(QHeaderView.Stretch)

        # get the data and set it to the models
        self.set_account_model()
        self.set_incoming_model()
        self.set_credit_card_model()

        # setup the vertical layouts
        grb_accounts_controls.setLayout(vbl_accounts_controls)
        grb_incomings_controls.setLayout(vbl_incomings_controls)
        grb_credit_cards_controls.setLayout(vbl_credit_cards_controls)

        vbl_accounts_controls.addWidget(lbl_account_mandatory_fields)
        vbl_accounts_controls.addLayout(frm_add_edit_accounts)
        vbl_accounts_controls.addWidget(self.lbl_account_error_message)
        vbl_accounts_controls.addWidget(btn_account_add)
        vbl_accounts_controls.addWidget(btn_account_edit)
        vbl_accounts_controls.addWidget(btn_account_delete)
        vbl_incomings_controls.addWidget(lbl_income_mandatory_fields)
        vbl_incomings_controls.addLayout(frm_add_edit_incomings)
        vbl_incomings_controls.addWidget(self.lbl_income_error_message)
        vbl_incomings_controls.addWidget(self.btn_incoming_add)
        vbl_incomings_controls.addWidget(btn_incoming_edit)
        vbl_incomings_controls.addWidget(btn_incoming_delete)
        vbl_credit_cards_controls.addWidget(lbl_credit_card_mandatory_fields)
        vbl_credit_cards_controls.addLayout(frm_add_edit_credit_cards)
        vbl_credit_cards_controls.addWidget(self.lbl_credit_card_error_message)
        vbl_credit_cards_controls.addWidget(btn_credit_card_add)
        vbl_credit_cards_controls.addWidget(btn_credit_card_edit)
        vbl_credit_cards_controls.addWidget(btn_credit_card_delete)

        vbl_accounts.addWidget(lbl_accounts_title)
        vbl_accounts.addWidget(self.tbl_accounts)
        vbl_accounts.addWidget(grb_accounts_controls)
        vbl_incomings.addWidget(lbl_incomes_title)
        vbl_incomings.addWidget(self.tbl_incomings)
        vbl_incomings.addWidget(grb_incomings_controls)
        vbl_credit_cards.addWidget(lbl_credit_cards_title)
        vbl_credit_cards.addWidget(self.tbl_credit_cards)
        vbl_credit_cards.addWidget(grb_credit_cards_controls)

        # setup the vertical layouts inside the horizontal layout
        hbl_incoming_outgoing.addLayout(vbl_accounts)
        hbl_incoming_outgoing.addLayout(vbl_incomings)
        hbl_incoming_outgoing.addLayout(vbl_credit_cards)

        # font setup
        fnt_title = lbl_accounts_title.font()
        fnt_title.setPointSize(14)
        fnt_title.setBold(True)
        lbl_accounts_title.setFont(fnt_title)
        lbl_incomes_title.setFont(fnt_title)
        lbl_credit_cards_title.setFont(fnt_title)

        fnt_error = self.lbl_account_error_message.font()
        fnt_error.setPointSize(12)
        fnt_error.setBold(True)
        self.lbl_account_error_message.setStyleSheet("color: rgb(250,0,0)")
        self.lbl_income_error_message.setStyleSheet("color: rgb(250,0,0)")
        self.lbl_credit_card_error_message.setStyleSheet("color: rgb(250,0,0)")

        # chose the horizontal layout as the main one
        self.setLayout(hbl_incoming_outgoing)

    def get_account_data(self):
        return {
            "name": self.lne_account_name.text(),
            "currency": self.cbx_account_currency.currentText(),
            "balance": self.dsp_account_balance.value() * 100,  # value is multiplied to become cents / pence
        }

    def get_income_source_data(self):
        return {
            "name": self.lne_incoming_name.text(),
            "account_name": self.cbx_incoming_account.currentText(),
            "recurrence_value": self.dsp_incoming_expected.value() * 100,
            "income_date": self.dte_incoming_date.date().toString("yyyy/MM/dd"),
            "currency": self.cbx_incoming_currency.currentText(),
            "recurrent": True if self.cbx_incoming_recurrent.currentText() == "Yes" else False,
            "recurrence": (
                self.cbx_incoming_recurrence.currentText()
                if self.cbx_incoming_recurrent.currentText() == "Yes"
                else None
            ),
        }

    def get_credit_card_data(self):
        return {
            "name": self.lne_credit_card_name.text(),
            "balance": self.dsp_credit_card_balance.value() * 100,
            "currency": self.cbx_credit_card_currency.currentText(),
            "credit_limit": self.dsp_credit_card_limit.value() * 100,
        }

    def populate_currencies(self):
        self.currency_list = self.presenter.get_currency()
        self.cbx_account_currency.clear()
        self.cbx_incoming_currency.clear()
        self.cbx_credit_card_currency.clear()
        self.cbx_account_currency.addItems([currency.name for currency in self.currency_list])
        self.cbx_incoming_currency.addItems([currency.name for currency in self.currency_list])
        self.cbx_credit_card_currency.addItems([currency.name for currency in self.currency_list])

    def populate_target_accounts(self):
        self.target_accounts = self.presenter.get_accounts()
        if len(self.target_accounts) > 0:
            self.btn_incoming_add.setEnabled(True)
        else:
            self.btn_incoming_add.setEnabled(False)
        self.cbx_incoming_account.clear()
        self.cbx_incoming_account.addItems(self.target_accounts)

    def populate_recurrence(self):
        self.recurrence_list = self.presenter.get_recurrence()
        self.cbx_incoming_recurrence.clear()
        self.cbx_incoming_recurrence.addItems([recurrence.value for recurrence in self.recurrence_list])

    def set_account_model(self):
        self.account_list = self.presenter.get_account_list("BANK")
        self.account_list_model = TableModel(
            [(account.name, f"{account.balance / 100} {account.currency.value}") for account in self.account_list],
            ["Name", "Balance"],
        )
        self.tbl_accounts.setModel(self.account_list_model)
        self.populate_target_accounts()

    def set_incoming_model(self):
        self.incoming_list = self.presenter.get_income_list()
        self.incoming_list_model = TableModel(
            [
                (income_source.name, f"{income_source.recurrence_value / 100} {income_source.currency.value}")
                for income_source in self.incoming_list
            ],
            ["Name", "Balance"],
        )
        self.tbl_incomings.setModel(self.incoming_list_model)

    def set_credit_card_model(self):
        self.credit_card_list = self.presenter.get_account_list("CARD")
        self.credit_card_list_model = TableModel(
            [
                (credit_card.name, f"{credit_card.balance / 100} {credit_card.currency.value}")
                for credit_card in self.credit_card_list
            ],
            ["Name", "Balance"],
        )
        self.tbl_credit_cards.setModel(self.credit_card_list_model)

    def on_account_table_view_selection(self, index):
        selected_row = index.row()
        account = self.account_list[selected_row]
        self.lne_account_name.setText(account.name)
        self.dsp_account_balance.setValue(account.balance / 100)
        self.cbx_account_currency.setCurrentText(account.currency.name)

    def on_incoming_table_view_selection(self, index):
        selected_row = index.row()
        income_source = self.incoming_list[selected_row]
        self.lne_incoming_name.setText(income_source.name)
        self.cbx_incoming_account.setCurrentText(income_source.account.name)
        self.dsp_incoming_expected.setValue(income_source.recurrence_value / 100)
        self.dte_incoming_date.setDate(income_source.income_date)
        self.cbx_incoming_currency.setCurrentText(income_source.currency.name)
        self.cbx_incoming_recurrence.setCurrentText(income_source.recurrence.value)

    def on_credit_card_table_view_selection(self, index):
        selected_row = index.row()
        credit_card = self.credit_card_list[selected_row]
        self.lne_credit_card_name.setText(credit_card.name)
        self.dsp_credit_card_balance.setValue(credit_card.balance / 100)
        self.cbx_credit_card_currency.setCurrentText(credit_card.currency.name)
        self.dsp_credit_card_limit.setValue(credit_card.credit_limit / 100)

    def on_recurrent_change(self):
        if self.cbx_incoming_recurrent.currentText() == "No":
            self.cbx_incoming_recurrence.setDisabled(True)
        else:
            self.cbx_incoming_recurrence.setDisabled(False)

    def set_account_error(self, message):
        self.lbl_account_error_message.setText(message)
        self.set_clear_timer()

    def set_income_error(self, message):
        self.lbl_income_error_message.setText(message)
        self.set_clear_timer()

    def set_credit_card_error(self, message):
        self.lbl_credit_card_error_message.setText(message)
        self.set_clear_timer()

    def set_clear_timer(self):
        timer = QTimer(self)
        timer.timeout.connect(lambda: self.reset_line_edit_text())
        timer.start(3 * 1000)

    def reset_line_edit_text(self):
        self.lbl_account_error_message.clear()
        self.lbl_income_error_message.clear()
        self.lbl_credit_card_error_message.clear()

    def on_account_currency_change(self):
        self.dsp_account_balance.setPrefix(f"{self.currency_list[self.cbx_account_currency.currentText()].value} ")

    def on_income_currency_change(self):
        self.dsp_incoming_expected.setPrefix(f"{self.currency_list[self.cbx_incoming_currency.currentText()].value} ")

    def on_credit_card_currency_change(self):
        self.dsp_credit_card_balance.setPrefix(
            f"{self.currency_list[self.cbx_credit_card_currency.currentText()].value} "
        )
        self.dsp_credit_card_limit.setPrefix(
            f"{self.currency_list[self.cbx_credit_card_currency.currentText()].value} "
        )

    def clear_account_data(self):
        self.lne_account_name.clear()
        self.cbx_account_currency.setCurrentIndex(1)
        self.dsp_account_balance.setValue(0.00)

    def clear_income_data(self):
        self.lne_incoming_name.clear()
        self.cbx_incoming_account.setCurrentIndex(1)
        self.cbx_incoming_currency.setCurrentIndex(1)
        self.dsp_incoming_expected.setValue(0.00)
        self.dte_incoming_date.clear()
        self.cbx_incoming_recurrence.setCurrentIndex(1)

    def clear_credit_card_data(self):
        self.lne_credit_card_name.clear()
        self.dsp_credit_card_balance.setValue(0.00)
        self.cbx_credit_card_currency.setCurrentIndex(1)
        self.dsp_credit_card_limit.setValue(0.00)

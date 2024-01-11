from PySide6.QtCore import QAbstractTableModel, QDate, QModelIndex, Qt, QTimer
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QDateEdit,
    QFormLayout,
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
        frm_add_edit_accounts = QFormLayout()
        frm_add_edit_incomings = QFormLayout()
        frm_add_edit_credit_cards = QFormLayout()
        self.lne_account_name = QLineEdit()
        self.lne_account_balance = QLineEdit()
        self.lne_incoming_name = QLineEdit()
        self.lne_incoming_expected = QLineEdit()
        self.lne_incoming_real = QLineEdit()
        self.lne_credit_card_name = QLineEdit()
        self.lne_credit_card_balance = QLineEdit()
        self.lne_credit_card_limit = QLineEdit()
        self.cbx_account_currency = QComboBox()
        self.cbx_incoming_account = QComboBox()
        self.cbx_incoming_currency = QComboBox()
        self.cbx_incoming_recurrence = QComboBox()
        self.cbx_credit_card_currency = QComboBox()
        self.lbl_account_error_message = QLabel("")
        self.lbl_income_error_message = QLabel("")
        self.lbl_credit_card_error_message = QLabel("")
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

        # setup of calendar
        min_date = QDate(QDate.currentDate().year(), 1, 1)
        max_date = QDate(QDate.currentDate().year(), 12, 31)
        self.dte_incoming_date.setCalendarPopup(True)
        self.dte_incoming_date.setDisplayFormat("dd/MM")
        self.dte_incoming_date.setDate(QDate.currentDate())
        self.dte_incoming_date.setDateRange(min_date, max_date)

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

        # add the entries into the form layout
        frm_add_edit_accounts.addRow("Account name", self.lne_account_name)
        frm_add_edit_accounts.addRow("Currency", self.cbx_account_currency)
        frm_add_edit_accounts.addRow("Balance", self.lne_account_balance)
        frm_add_edit_accounts.addWidget(self.lbl_account_error_message)
        frm_add_edit_incomings.addRow("Income source", self.lne_incoming_name)
        frm_add_edit_incomings.addRow("Target account", self.cbx_incoming_account)
        frm_add_edit_incomings.addRow("Expected income", self.lne_incoming_expected)
        frm_add_edit_incomings.addRow("Expected income date", self.dte_incoming_date)
        frm_add_edit_incomings.addRow("Income currency", self.cbx_incoming_currency)
        frm_add_edit_incomings.addRow("Recurrence", self.cbx_incoming_recurrence)
        frm_add_edit_incomings.addWidget(self.lbl_income_error_message)
        frm_add_edit_credit_cards.addRow("Credit card name", self.lne_credit_card_name)
        frm_add_edit_credit_cards.addRow("Credit card balance", self.lne_credit_card_balance)
        frm_add_edit_credit_cards.addRow("Credit card currency", self.cbx_credit_card_currency)
        frm_add_edit_credit_cards.addRow("Credit limit", self.lne_credit_card_limit)
        frm_add_edit_credit_cards.addWidget(self.lbl_credit_card_error_message)

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
        vbl_accounts.addWidget(self.tbl_accounts)
        vbl_accounts.addLayout(frm_add_edit_accounts)
        vbl_accounts.addLayout(hbl_accounts_controls)
        vbl_incomings.addWidget(self.tbl_incomings)
        vbl_incomings.addLayout(frm_add_edit_incomings)
        vbl_incomings.addLayout(hbl_incomings_controls)
        vbl_credit_cards.addWidget(self.tbl_credit_cards)
        vbl_credit_cards.addLayout(frm_add_edit_credit_cards)
        vbl_credit_cards.addLayout(hbl_credit_cards_controls)

        # setup the vertical layouts inside the horizontal layout
        hbl_incoming_outgoing.addLayout(vbl_accounts, 1)
        hbl_incoming_outgoing.addLayout(vbl_incomings, 1)
        hbl_incoming_outgoing.addLayout(vbl_credit_cards, 1)

        # chose the horizontal layout as the main one
        self.setLayout(hbl_incoming_outgoing)

    def get_account_data(self):
        return {
            "name": self.lne_account_name.text(),
            "currency": self.cbx_account_currency.currentText(),
            "balance": self.lne_account_balance.text(),
        }

    def get_income_source_data(self):
        return {
            "name": self.lne_incoming_name.text(),
            "account_name": self.cbx_incoming_account.currentText(),
            "expected_income_value": self.lne_incoming_expected.text(),
            "income_date": self.dte_incoming_date.date().toString("yyyy/MM/dd"),
            "currency": self.cbx_incoming_currency.currentText(),
            "recurrence": self.cbx_incoming_recurrence.currentText(),
        }

    def get_credit_card_data(self):
        return {
            "name": self.lne_credit_card_name.text(),
            "balance": self.lne_credit_card_balance.text(),
            "currency": self.cbx_credit_card_currency.currentText(),
            "credit_limit": self.lne_credit_card_limit.text(),
        }

    def populate_currencies(self):
        currencies = self.presenter.get_currency()
        self.cbx_account_currency.clear()
        self.cbx_incoming_currency.clear()
        self.cbx_credit_card_currency.clear()
        self.cbx_account_currency.addItems(currencies)
        self.cbx_incoming_currency.addItems(currencies)
        self.cbx_credit_card_currency.addItems(currencies)

    def populate_target_accounts(self):
        self.target_accounts = self.presenter.get_target_accounts()
        if len(self.target_accounts) > 0:
            self.btn_incoming_add.setEnabled(True)
        else:
            self.btn_incoming_add.setEnabled(False)
        self.cbx_incoming_account.clear()
        self.cbx_incoming_account.addItems(self.target_accounts)

    def populate_recurrence(self):
        recurrence = self.presenter.get_recurrence()
        self.cbx_incoming_recurrence.clear()
        self.cbx_incoming_recurrence.addItems(recurrence)

    def set_account_model(self):
        self.account_list = self.presenter.get_account_list("BANK")
        self.account_list_model = TableModel(
            [(account.name, f"{account.balance} {account.currency.value}") for account in self.account_list],
            ["Name", "Balance"],
        )
        self.tbl_accounts.setModel(self.account_list_model)
        self.populate_target_accounts()

    def set_incoming_model(self):
        self.incoming_list = self.presenter.get_income_list()
        self.incoming_list_model = TableModel(
            [
                (income_source.name, f"{income_source.expected_income_value} {income_source.currency.value}")
                for income_source in self.incoming_list
            ],
            ["Name", "Balance"],
        )
        self.tbl_incomings.setModel(self.incoming_list_model)

    def set_credit_card_model(self):
        self.credit_card_list = self.presenter.get_account_list("CARD")
        self.credit_card_list_model = TableModel(
            [
                (credit_card.name, f"{credit_card.balance} {credit_card.currency.value}")
                for credit_card in self.credit_card_list
            ],
            ["Name", "Balance"],
        )
        self.tbl_credit_cards.setModel(self.credit_card_list_model)

    def on_account_table_view_selection(self, index):
        selected_row = index.row()
        account = self.account_list[selected_row]
        self.lne_account_name.setText(account.name)
        self.lne_account_balance.setText(str(account.balance))
        self.cbx_account_currency.setCurrentText(account.currency.name)

    def on_incoming_table_view_selection(self, index):
        selected_row = index.row()
        income_source = self.incoming_list[selected_row]
        self.lne_incoming_name.setText(income_source.name)
        self.cbx_incoming_account.setCurrentText(income_source.account.name)
        self.lne_incoming_expected.setText(str(income_source.expected_income_value))
        self.dte_incoming_date.setDate(income_source.income_date)
        self.cbx_incoming_currency.setCurrentText(income_source.currency.name)
        self.cbx_incoming_recurrence.setCurrentText(income_source.recurrence.value)

    def on_credit_card_table_view_selection(self, index):
        selected_row = index.row()
        credit_card = self.credit_card_list[selected_row]
        self.lne_credit_card_name.setText(credit_card.name)
        self.lne_credit_card_balance.setText(str(credit_card.balance))
        self.cbx_credit_card_currency.setCurrentText(credit_card.currency.name)
        self.lne_credit_card_limit.setText(str(credit_card.credit_limit))

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

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt, QTimer
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
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

from ezbudget.view.styles import (
    DateSetup,
    DoubleSpinBox,
    ErrorMessage,
    MainTitle,
    SecondaryTitle,
)


class TableModel(QAbstractTableModel):
    def __init__(self, data: list, headers: list, presenter_data_fetch):
        super().__init__()
        self._data: list = data
        self.headers: list = headers
        self.data_fetch = presenter_data_fetch

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(self._data[index.row()][index.column()])

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]

    def addData(self, data):
        self.beginInsertRows(QModelIndex(), len(self._data), len(self._data))
        self._data.append(data)
        self.endInsertRows()

    def getData(self):
        response = []
        for data in self._data:
            response.append(data)
        return response

    def updateAccounts(self):
        self.beginResetModel()
        data_list = self.data_fetch()
        self._data = [(data.name, f"{data.balance / 100} {data.currency.value}") for data in data_list]
        self.endResetModel()


class IncomingOutgoing(QWidget):
    def __init__(self, parent, presenter):
        super().__init__()
        self.presenter = presenter
        self._parent = parent

        # instances of necessary widgets
        hbl_incoming_outgoing = QHBoxLayout()
        hbl_accounts_controls = QHBoxLayout()
        hbl_incomings_controls = QHBoxLayout()
        hbl_credit_cards_controls = QHBoxLayout()
        vbl_main_layout = QVBoxLayout()
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
        lbl_account_mandatory_fields = QLabel("Fields with an asterisk (*) are mandatory")
        lbl_income_mandatory_fields = QLabel("Fields with an asterisk (*) are mandatory")
        lbl_credit_card_mandatory_fields = QLabel("Fields with an asterisk (*) are mandatory")
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

        self.clear_timer = None
        lbl_title_manage_accounts = MainTitle("Manage accounts")
        lbl_accounts_title = SecondaryTitle("Cash & Bank Accounts")
        lbl_incomes_title = SecondaryTitle("Income sources")
        lbl_credit_cards_title = SecondaryTitle("Credit cards")
        self.lbl_account_error_message = ErrorMessage("")
        self.lbl_income_error_message = ErrorMessage("")
        self.lbl_credit_card_error_message = ErrorMessage("")
        self.dsp_account_balance = DoubleSpinBox()
        self.dsp_incoming_expected = DoubleSpinBox()
        self.dsp_credit_card_balance = DoubleSpinBox()
        self.dsp_credit_card_limit = DoubleSpinBox()
        self.dte_incoming_date = DateSetup("dd/MM", "yearly")

        # setup and link models to tables
        # account model and table
        self.account_list = self.presenter.get_account_list("BANK")
        self.account_list_model = TableModel(
            [(account.name, f"{account.balance / 100} {account.currency.value}") for account in self.account_list],
            ["Name", "Balance"],
            lambda: self.presenter.get_account_list("BANK"),
        )
        self.tbl_accounts.setModel(self.account_list_model)
        # incoming source model and table
        self.incoming_list = self.presenter.get_income_list()
        self.incoming_list_model = TableModel(
            [
                (income_source.name, f"{income_source.recurrence_value / 100} {income_source.currency.value}")
                for income_source in self.incoming_list
            ],
            ["Name", "Balance"],
            self.presenter.get_income_list,
        )
        self.tbl_incomings.setModel(self.incoming_list_model)
        # credit card model and table
        self.credit_card_list = self.presenter.get_account_list("CARD")
        self.credit_card_list_model = TableModel(
            [
                (credit_card.name, f"{credit_card.balance / 100} {credit_card.currency.value}")
                for credit_card in self.credit_card_list
            ],
            ["Name", "Balance"],
            lambda: self.presenter.get_account_list("CARD"),
        )
        self.tbl_credit_cards.setModel(self.credit_card_list_model)

        # setup combobox and buttons
        self.populate_currencies()
        self.populate_target_accounts()
        self.populate_recurrence()
        btn_account_edit.setEnabled(False)
        btn_account_delete.setEnabled(False)
        btn_account_add.clicked.connect(lambda: self.create_account("BANK"))
        btn_incoming_edit.setEnabled(False)
        btn_incoming_delete.setEnabled(False)
        self.btn_incoming_add.clicked.connect(self.create_income_source)
        btn_credit_card_edit.setEnabled(False)
        btn_credit_card_delete.setEnabled(False)
        btn_credit_card_add.clicked.connect(lambda: self.create_account("CARD"))

        # organize the buttons into the controls layout
        accounts_controls = [btn_account_add, btn_account_edit, btn_account_delete]
        for btn in accounts_controls:
            hbl_accounts_controls.addWidget(btn)
        incoming_controls = [self.btn_incoming_add, btn_incoming_edit, btn_incoming_delete]
        for btn in incoming_controls:
            hbl_incomings_controls.addWidget(btn)
        credit_card_controls = [btn_credit_card_add, btn_credit_card_edit, btn_credit_card_delete]
        for btn in credit_card_controls:
            hbl_credit_cards_controls.addWidget(btn)

        # configure entries
        self.lne_account_name.setPlaceholderText("Enter account name...")
        self.cbx_account_currency.currentTextChanged.connect(self.on_account_currency_change)
        self.on_account_currency_change()
        self.lne_incoming_name.setPlaceholderText("Enter income name...")
        self.cbx_incoming_currency.currentTextChanged.connect(self.on_income_currency_change)
        self.on_income_currency_change()
        self.lne_credit_card_name.setPlaceholderText("Enter card name...")
        self.cbx_credit_card_currency.currentTextChanged.connect(self.on_credit_card_currency_change)
        self.on_credit_card_currency_change()

        # add entries to form layouts
        add_edit_accounts = {
            "Name (*)": self.lne_account_name,
            "Currency (*)": self.cbx_account_currency,
            "Balance": self.dsp_account_balance,
        }
        for key, value in add_edit_accounts.items():
            frm_add_edit_accounts.addRow(key, value)

        add_edit_incoming = {
            "Name (*)": self.lne_incoming_name,
            "Account (*)": self.cbx_incoming_account,
            "Currency (*)": self.cbx_incoming_currency,
            "Expected income": self.dsp_incoming_expected,
            "Expected date": self.dte_incoming_date,
            "Recurrent": self.cbx_incoming_recurrent,
            "Recurrence": self.cbx_incoming_recurrence,
        }
        self.cbx_incoming_recurrent.addItems(["Yes", "No"])
        self.cbx_incoming_recurrent.currentIndexChanged.connect(self.on_recurrent_change)
        for key, value in add_edit_incoming.items():
            frm_add_edit_incomings.addRow(key, value)

        add_edit_credit_cards = {
            "Name (*)": self.lne_credit_card_name,
            "Balance (*)": self.dsp_credit_card_balance,
            "Currency": self.cbx_credit_card_currency,
            "Credit limit": self.dsp_credit_card_limit,
        }
        for key, value in add_edit_credit_cards.items():
            frm_add_edit_credit_cards.addRow(key, value)

        # setup the tables
        table_list = [self.tbl_accounts, self.tbl_incomings, self.tbl_credit_cards]
        for tbl in table_list:
            tbl.setSelectionMode(QAbstractItemView.SingleSelection)
            tbl.setSelectionBehavior(QAbstractItemView.SelectRows)
            tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            tbl.setAlternatingRowColors(True)
        self.tbl_accounts.clicked.connect(self.on_account_table_view_selection)
        self.tbl_incomings.clicked.connect(self.on_incoming_table_view_selection)
        self.tbl_credit_cards.clicked.connect(self.on_credit_card_table_view_selection)

        # signals from the models to update other elements
        self.account_list_model.rowsInserted.connect(lambda: self.on_model_row_inserted("BANK"))
        self.incoming_list_model.rowsInserted.connect(lambda: self.on_model_row_inserted("INCOME"))
        self.credit_card_list_model.rowsInserted.connect(lambda: self.on_model_row_inserted("CARD"))

        # setup the vertical layouts
        grb_accounts_controls.setLayout(vbl_accounts_controls)
        grb_incomings_controls.setLayout(vbl_incomings_controls)
        grb_credit_cards_controls.setLayout(vbl_credit_cards_controls)

        # setup the controls widgets
        # accounts controls
        accounts_layout_setup = [
            lbl_account_mandatory_fields,
            frm_add_edit_accounts,
            self.lbl_account_error_message,
            btn_account_add,
            btn_account_edit,
            btn_account_delete,
        ]
        for widget in accounts_layout_setup:
            if isinstance(widget, QFormLayout):
                vbl_accounts_controls.addLayout(widget)
            else:
                vbl_accounts_controls.addWidget(widget)
        # income source controls
        incoming_layout_setup = [
            lbl_income_mandatory_fields,
            frm_add_edit_incomings,
            self.lbl_income_error_message,
            self.btn_incoming_add,
            btn_incoming_edit,
            btn_incoming_delete,
        ]
        for widget in incoming_layout_setup:
            if isinstance(widget, QFormLayout):
                vbl_incomings_controls.addLayout(widget)
            else:
                vbl_incomings_controls.addWidget(widget)
        # credit card controls
        credit_card_layout_setup = [
            lbl_credit_card_mandatory_fields,
            frm_add_edit_credit_cards,
            self.lbl_credit_card_error_message,
            btn_credit_card_add,
            btn_credit_card_edit,
            btn_credit_card_delete,
        ]
        for widget in credit_card_layout_setup:
            if isinstance(widget, QFormLayout):
                vbl_credit_cards_controls.addLayout(widget)
            else:
                vbl_credit_cards_controls.addWidget(widget)

        # setup the vertical layouts
        # accounts layouts
        accounts_layouts = [lbl_accounts_title, self.tbl_accounts, grb_accounts_controls]
        for w in accounts_layouts:
            vbl_accounts.addWidget(w)
        # income sources layouts
        income_sources_layouts = [lbl_incomes_title, self.tbl_incomings, grb_incomings_controls]
        for w in income_sources_layouts:
            vbl_incomings.addWidget(w)
        # credit cards layouts
        credit_card_layouts = [lbl_credit_cards_title, self.tbl_credit_cards, grb_credit_cards_controls]
        for w in credit_card_layouts:
            vbl_credit_cards.addWidget(w)

        # setup the vertical layouts inside the horizontal layout
        hbl_incoming_outgoing.addLayout(vbl_accounts)
        hbl_incoming_outgoing.addLayout(vbl_incomings)
        hbl_incoming_outgoing.addLayout(vbl_credit_cards)

        # setup everything on the main layout
        vbl_main_layout.addWidget(lbl_title_manage_accounts)
        vbl_main_layout.addLayout(hbl_incoming_outgoing)

        # chose the horizontal layout as the main one
        self.setLayout(vbl_main_layout)

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
        accounts = self.account_list_model.getData()
        if len(accounts) > 0:
            self.btn_incoming_add.setEnabled(True)
        else:
            self.btn_incoming_add.setEnabled(False)
        self.cbx_incoming_account.clear()
        self.cbx_incoming_account.addItems([account[0] for account in accounts])

    def populate_recurrence(self):
        self.recurrence_list = self.presenter.get_recurrence()
        self.cbx_incoming_recurrence.clear()
        self.cbx_incoming_recurrence.addItems([recurrence.value for recurrence in self.recurrence_list])

    def create_account(self, type: str) -> None:
        data = self.get_account_data()
        new_account = self.presenter.create_account(data, type)
        if isinstance(new_account, str):
            self.set_error_message(type, new_account)
        else:
            insert_data = [new_account.name, f"{new_account.balance / 100} {new_account.currency.value}"]
            if type == "BANK":
                self.account_list_model.addData(insert_data)
            if type == "CARD":
                self.credit_card_list_model.addData(insert_data)

    def create_income_source(self):
        data = self.get_income_source_data()
        new_income_source = self.presenter.create_income(data)
        if isinstance(new_income_source, str):
            self.set_error_message("INCOME", new_income_source)
        else:
            self.incoming_list_model.addData(
                [new_income_source.name, f"{new_income_source.balance / 100} {new_income_source.currency.value}"]
            )

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

    def set_error_message(self, type: str, message: str) -> None:
        if type == "BANK":
            self.lbl_account_error_message.setText(message)
        if type == "INCOME":
            self.lbl_income_error_message.setText(message)
        if type == "CARD":
            self.lbl_credit_card_error_message.setText(message)
        self.set_clear_timer()

    def set_clear_timer(self):
        if not self.clear_timer:
            self.clear_timer = QTimer(self)
            self.clear_timer.timeout.connect(self.reset_line_edit_text)
            # Start the timer
            self.clear_timer.start(3 * 1000)
        else:
            # Restart the timer if it already exists
            self.clear_timer.start(3 * 1000)

    def reset_line_edit_text(self):
        self.lbl_account_error_message.clear()
        self.lbl_income_error_message.clear()
        self.lbl_credit_card_error_message.clear()
        # Stop the timer after clearing the messages
        if self.clear_timer:
            self.clear_timer.stop()

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
        self.cbx_account_currency.setCurrentIndex(0)
        self.dsp_account_balance.setValue(0.00)

    def clear_income_data(self):
        self.lne_incoming_name.clear()
        self.cbx_incoming_account.setCurrentIndex(0)
        self.cbx_incoming_currency.setCurrentIndex(0)
        self.dsp_incoming_expected.setValue(0.00)
        self.dte_incoming_date.clear()
        self.cbx_incoming_recurrence.setCurrentIndex(0)

    def clear_credit_card_data(self):
        self.lne_credit_card_name.clear()
        self.dsp_credit_card_balance.setValue(0.00)
        self.cbx_credit_card_currency.setCurrentIndex(0)
        self.dsp_credit_card_limit.setValue(0.00)

    def on_model_row_inserted(self, type: str):
        if type == "BANK":
            self.populate_target_accounts()
            self.clear_account_data()
        if type == "INCOME":
            self.clear_income_data()
        if type == "CARD":
            self.clear_credit_card_data()

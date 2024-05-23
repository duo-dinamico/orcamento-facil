from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt, QTimer
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLineEdit,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from ezbudget.model import AccountTypeEnum
from ezbudget.view.models import CurrencyItem
from ezbudget.view.styles import DoubleSpinBox, ErrorMessage, MadatoryFields, MainTitle


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
        formatted_data = []
        for data in data_list:
            currency_amount = data.balance / 100
            currency_with_value = CurrencyItem(data.currency, currency_amount)
            formatted_data.append((data.name, currency_with_value.valueWithCurrency(), data.account_type.value))
        self._data = formatted_data
        self.endResetModel()


class Accounts(QWidget):
    def __init__(self, parent, presenter):
        super().__init__()
        self.presenter = presenter
        self._parent = parent

        # instances of necessary widgets
        hbl_accounts = QHBoxLayout()
        vbl_main_layout = QVBoxLayout()
        vbl_accounts = QVBoxLayout()
        vbl_accounts_controls = QVBoxLayout()
        frm_add_edit_accounts = QFormLayout()
        grb_accounts_controls = QGroupBox("Manage accounts")
        self.lne_account_name = QLineEdit()
        self.cbx_account_currency = QComboBox()
        self.cbx_account_type = QComboBox()
        btn_account_add = QPushButton("Add account")
        btn_account_edit = QPushButton("Edit account")
        btn_account_delete = QPushButton("Delete account")
        self.tbl_accounts = QTableView()

        self.clear_timer = None
        lbl_title_manage_accounts = MainTitle("Accounts and Credit Cards")
        self.lbl_account_error_message = ErrorMessage("")
        lbl_account_mandatory_fields = MadatoryFields("Fields with an asterisk (*) are mandatory")
        self.dsp_account_balance = DoubleSpinBox()
        self.dsp_credit_card_limit = DoubleSpinBox()

        self.starting_setup()

        # setup and link models to tables
        self.account_list: list = self.presenter.get_account_list()
        account_list_data = self.format_model_data(self.account_list)
        self.account_list_model = TableModel(
            account_list_data,
            ["Name", "Balance", "Type"],
            lambda: self.presenter.get_account_list(),
        )
        self.tbl_accounts.setModel(self.account_list_model)

        # setup combobox and buttons
        btn_account_edit.setEnabled(False)
        btn_account_delete.setEnabled(False)
        btn_account_add.clicked.connect(self.create_account)

        # organize the buttons into the controls layout
        accounts_controls = [btn_account_add, btn_account_edit, btn_account_delete]
        for btn in accounts_controls:
            vbl_accounts_controls.addWidget(btn)

        # configure entries
        self.lne_account_name.setPlaceholderText("Enter account name...")
        self.cbx_account_type.addItems([e.value for e in AccountTypeEnum])
        self.cbx_account_currency.currentTextChanged.connect(self.on_account_currency_change)

        # add entries to form layouts
        add_edit_accounts = {
            "Name (*)": self.lne_account_name,
            "Account Type (*)": self.cbx_account_type,
            "Currency (*)": self.cbx_account_currency,
            "Balance": self.dsp_account_balance,
            "Credit limit": self.dsp_credit_card_limit,
        }
        for key, value in add_edit_accounts.items():
            frm_add_edit_accounts.addRow(key, value)

        # setup the tables
        self.tbl_accounts.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tbl_accounts.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tbl_accounts.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tbl_accounts.setAlternatingRowColors(True)
        self.tbl_accounts.clicked.connect(self.on_account_table_view_selection)

        # signals from the models to update other elements
        self.account_list_model.rowsInserted.connect(self.on_model_row_inserted)

        # setup the vertical layouts
        grb_accounts_controls.setLayout(vbl_accounts)

        # setup the controls widgets
        vbl_accounts.addWidget(lbl_account_mandatory_fields)
        vbl_accounts.addLayout(frm_add_edit_accounts)
        vbl_accounts.insertStretch(2, 1)
        vbl_accounts.addWidget(self.lbl_account_error_message)
        vbl_accounts.addLayout(vbl_accounts_controls)

        # setup the vertical layouts
        hbl_accounts.addWidget(self.tbl_accounts, 2)
        hbl_accounts.addWidget(grb_accounts_controls, 1)

        # setup everything on the main layout
        vbl_main_layout.addWidget(lbl_title_manage_accounts)
        vbl_main_layout.addLayout(hbl_accounts)

        # chose the horizontal layout as the main one
        self.setLayout(vbl_main_layout)

    def starting_setup(self):
        self.populate_currencies()
        self.on_account_currency_change()

    def get_account_data(self):
        return {
            "name": self.lne_account_name.text(),
            "account_type": self.cbx_account_type.currentText(),
            "currency_id": self.selected_account_currency.getId(),
            "balance": self.dsp_account_balance.value() * 100,  # value is multiplied to become cents / pence
            "credit_limit": self.dsp_credit_card_limit.value() * 100,
        }

    def populate_currencies(self):
        all_currencies = self.presenter.get_currency()
        self.currency_list = [CurrencyItem(currency) for currency in all_currencies]
        self.cbx_account_currency.clear()
        self.cbx_account_currency.addItems([currency.getName() for currency in self.currency_list])

    def create_account(self) -> None:
        data = self.get_account_data()
        new_account = self.presenter.create_account(data)
        if isinstance(new_account, str):
            self.set_error_message(new_account)
        else:
            currency_amount = new_account.balance / 100
            currency_with_value = CurrencyItem(new_account.currency, currency_amount)
            insert_data = [new_account.name, currency_with_value.valueWithCurrency(), new_account.account_type.value]

            self.account_list.append(new_account)
            self.account_list_model.addData(insert_data)

    def on_account_table_view_selection(self, index):
        selected_row = index.row()
        account = self.account_list[selected_row]
        self.lne_account_name.setText(account.name)
        self.dsp_account_balance.setValue(account.balance / 100)
        self.cbx_account_type.setCurrentText(account.account_type.value)
        self.cbx_account_currency.setCurrentText(account.currency.name)
        self.dsp_credit_card_limit.setValue(account.credit_limit / 100 if account.credit_limit is not None else 0)

    def set_error_message(self, message: str) -> None:
        self.lbl_account_error_message.setText(message)
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
        self.lbl_account_error_message.setText("")
        # Stop the timer after clearing the messages
        if self.clear_timer:
            self.clear_timer.stop()

    def on_account_currency_change(self):
        current_currency = self.cbx_account_currency.currentText()
        for currency in self.currency_list:
            if currency.getName() == current_currency:
                self.selected_account_currency = currency
                self.dsp_account_balance.setPrefix(currency.getSymbol())
                self.dsp_credit_card_limit.setPrefix(currency.getSymbol())

    def clear_account_data(self):
        self.lne_account_name.clear()
        self.cbx_account_currency.setCurrentIndex(0)
        self.dsp_account_balance.setValue(0.00)
        self.dsp_credit_card_limit.setValue(0.00)

    def on_model_row_inserted(self):
        self.clear_account_data()

    def format_model_data(self, data_list: list) -> list:
        response = []
        for data in data_list:
            currency_with_value = CurrencyItem(data.currency, data.balance / 100)
            response.append((data.name, currency_with_value.valueWithCurrency(), data.account_type.value))
        return response

from PySide6.QtCore import QAbstractTableModel, QDate, QDateTime, QModelIndex, Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDoubleSpinBox,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QLineEdit,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)


class TableModel(QAbstractTableModel):
    def __init__(self, transactions):
        super().__init__()
        self.transactions = transactions
        self.headers = ["Account", "Category", "Date", "Type", "Value", "Description"]

    def rowCount(self, parent=QModelIndex()):
        return len(self.transactions)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        row_data = self.transactions[index.row()]
        if role == Qt.DisplayRole:
            if index.column() == 0:  # Account column
                return str(row_data.account.name)
            elif index.column() == 1:  # Category column
                return f"{row_data.subcategory.category.name} - {row_data.subcategory.name}"
            elif index.column() == 2:  # Date column
                date_time = QDateTime.fromString(str(row_data.date), "yyyy-MM-dd hh:mm:ss")
                return date_time.toString("dd/MM/yyyy")
            elif index.column() == 3:  # Transaction type column
                return str(row_data.transaction_type.name)
            elif index.column() == 4:  # Value column
                return f"{row_data.currency.value} {row_data.value / 100}"
            elif index.column() == 5:  # Description column
                return str(row_data.description)

        elif role == Qt.UserRole:  # Storing transaction ID in UserRole
            return row_data.id

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]


class Transactions(QWidget):
    def __init__(self, presenter):
        super().__init__()
        self.presenter = presenter

        # instances of necessary widgets
        hbl_transactions = QHBoxLayout()
        vbl_add_edit_transactions = QVBoxLayout()
        frm_add_edit_transactions = QFormLayout()
        self.cbx_account = QComboBox()
        self.cbx_subcategories = QComboBox()
        self.cbx_currencies = QComboBox()
        self.cbx_transaction_type = QComboBox()
        self.cbx_target_account = QComboBox()
        self.chk_transfer_account_toggle = QCheckBox()
        self.dte_transaction_date = QDateEdit()
        self.lne_description = QLineEdit()
        self.btn_add_transaction = QPushButton("Add transaction")
        self.btn_edit_transaction = QPushButton("Edit transaction")
        self.btn_delete_transaction = QPushButton("Delete transaction")
        self.btn_clear = QPushButton("Clear")
        self.tbl_transactions = QTableView()
        self.dsp_value = QDoubleSpinBox()
        self.dsp_recurring_value = QDoubleSpinBox()

        # setup the tables
        self.tbl_transactions.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tbl_transactions.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tbl_transactions.clicked.connect(self.on_table_view_selection)
        table_header = self.tbl_transactions.horizontalHeader()
        table_header.setSectionResizeMode(QHeaderView.Stretch)

        # get the data and set it to the models
        self.populate_accounts()
        self.populate_subcategories()
        self.populate_transaction_types()
        self.on_subcategory_change()
        self.set_transactions_model()

        # target accounts setup
        self.cbx_target_account.setEnabled(False)
        self.cbx_account.currentTextChanged.connect(self.on_transfer_account_toggle)
        self.chk_transfer_account_toggle.stateChanged.connect(self.on_transfer_account_toggle)

        # setup of calendar
        min_date = QDate(QDate.currentDate().year(), QDate.currentDate().month(), 1)
        max_date = QDate(QDate.currentDate().year(), QDate.currentDate().month(), min_date.daysInMonth())
        self.dte_transaction_date.setCalendarPopup(True)
        self.dte_transaction_date.setDisplayFormat("dd/MM/yyyy")
        self.dte_transaction_date.setDate(QDate.currentDate())
        self.dte_transaction_date.setDateRange(min_date, max_date)
        self.dte_transaction_date.setAlignment(Qt.AlignmentFlag.AlignRight)

        # setup the frame
        frm_add_edit_transactions.addRow("Account", self.cbx_account)
        frm_add_edit_transactions.addRow("Is account transfer", self.chk_transfer_account_toggle)
        frm_add_edit_transactions.addRow("Target account", self.cbx_target_account)
        frm_add_edit_transactions.addRow("Category", self.cbx_subcategories)
        frm_add_edit_transactions.addRow("Recurring value", self.dsp_recurring_value)
        frm_add_edit_transactions.addRow("Date", self.dte_transaction_date)
        frm_add_edit_transactions.addRow("Currency", self.cbx_currencies)
        frm_add_edit_transactions.addRow("Transaction type", self.cbx_transaction_type)
        frm_add_edit_transactions.addRow("Value", self.dsp_value)
        frm_add_edit_transactions.addRow("Description", self.lne_description)

        # configure entries
        self.populate_currencies()
        self.dsp_recurring_value.setEnabled(False)
        self.dsp_recurring_value.setRange(-999999.99, 999999.99)
        self.dsp_recurring_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.dsp_value.setRange(-999999.99, 999999.99)
        self.dsp_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.dsp_value.setPrefix(f"{self.currency_list[self.cbx_currencies.currentText()].value} ")
        self.cbx_currencies.currentTextChanged.connect(self.on_currency_change)

        # setup the add / edit frame
        vbl_add_edit_transactions.addLayout(frm_add_edit_transactions)
        vbl_add_edit_transactions.addWidget(self.btn_add_transaction)
        vbl_add_edit_transactions.addWidget(self.btn_edit_transaction)
        vbl_add_edit_transactions.addWidget(self.btn_delete_transaction)
        vbl_add_edit_transactions.addWidget(self.btn_clear)
        self.btn_edit_transaction.setEnabled(False)
        self.btn_delete_transaction.setEnabled(False)
        self.btn_clear.setEnabled(False)
        self.btn_add_transaction.clicked.connect(lambda: self.presenter.create_transaction(self.get_transaction_data()))
        self.btn_edit_transaction.clicked.connect(
            lambda: self.presenter.update_transaction(
                self.transaction_id,
                self.get_transaction_data(),
                self.current_value,
                self.current_account_id,
                self.transaction_type,
            )
        )
        self.btn_delete_transaction.clicked.connect(
            lambda: self.presenter.remove_transaction(
                self.get_transaction_data(), self.transaction_id, self.current_account_id, self.target_account_id
            )
        )
        self.btn_clear.clicked.connect(self.clear_fields)
        self.cbx_subcategories.currentTextChanged.connect(self.on_subcategory_change)

        # setup the horizontal layouts
        hbl_transactions.addWidget(self.tbl_transactions, 2)
        hbl_transactions.addLayout(vbl_add_edit_transactions, 1)

        # chose the horizontal layout as the main one
        self.setLayout(hbl_transactions)

    def populate_currencies(self):
        self.currency_list = self.presenter.get_currency()
        self.cbx_currencies.clear()
        self.cbx_currencies.addItems([currency.name for currency in self.currency_list])

    def populate_transaction_types(self):
        self.transaction_types_list = self.presenter.get_transaction_types()
        self.cbx_transaction_type.clear()
        self.cbx_transaction_type.addItems([transaction_type.name for transaction_type in self.transaction_types_list])

    def on_table_view_selection(self, index):
        selected_row = index.row()
        transaction = self.transactions_list[selected_row]
        selected_index = self.tbl_transactions.selectionModel().currentIndex()
        self.current_value = transaction.value
        self.current_account_id = transaction.account.id
        self.transaction_type = transaction.transaction_type
        self.transaction_id = selected_index.siblingAtColumn(0).data(Qt.UserRole)
        self.cbx_account.setCurrentText(transaction.account.name)
        self.cbx_subcategories.setCurrentText(
            f"{transaction.subcategory.category.name} - {transaction.subcategory.name}"
        )
        self.cbx_transaction_type.setCurrentText(transaction.transaction_type.name)
        self.cbx_currencies.setCurrentText(transaction.currency.name)
        self.dte_transaction_date.setDate(transaction.date)
        self.dsp_value.setValue(transaction.value / 100)
        self.lne_description.setText(transaction.description)
        self.btn_add_transaction.setText("Duplicate transaction")
        self.btn_edit_transaction.setEnabled(True)
        self.btn_delete_transaction.setEnabled(True)
        self.btn_clear.setEnabled(True)
        if transaction.transaction_type.name == "Transfer":
            self.chk_transfer_account_toggle.setChecked(True)
            self.cbx_target_account.setCurrentText(transaction.target_account.name)
            self.target_account_id = transaction.target_account.id
        else:
            self.chk_transfer_account_toggle.setChecked(False)

    def get_transaction_data(self):
        data = {
            "account_name": self.cbx_account.currentText(),
            "target_account_name": self.cbx_target_account.currentText(),
            "subcategory_name": self.cbx_subcategories.currentText(),
            "date": self.dte_transaction_date.date().toString("yyyy/MM/dd"),
            "currency": self.cbx_currencies.currentText(),
            "transaction_type": self.cbx_transaction_type.currentText(),
            "value": self.dsp_value.value() * 100,
            "description": self.lne_description.text(),
        }
        return data

    def populate_accounts(self):
        self.accounts = self.presenter.get_accounts()
        self.cbx_account.clear()
        self.cbx_account.addItems(self.accounts)

    def populate_target_accounts(self):
        self.target_accounts = self.presenter.get_accounts()
        accounts_without_origin = []
        for account in self.target_accounts:
            if self.cbx_account.currentText() != account:
                accounts_without_origin.append(account)
        self.cbx_target_account.clear()
        self.cbx_target_account.addItems(accounts_without_origin)

    def on_transfer_account_toggle(self):
        if self.chk_transfer_account_toggle.isChecked():
            self.cbx_target_account.setEnabled(True)
            self.cbx_transaction_type.setEnabled(False)
            self.cbx_transaction_type.setCurrentText("Transfer")
            self.populate_target_accounts()
        else:
            self.cbx_target_account.clear()
            self.cbx_transaction_type.setEnabled(True)
            self.populate_transaction_types()

    def populate_subcategories(self):
        self.subcategories = self.presenter.get_user_subcategory_list()
        self.on_subcategory_change()
        self.cbx_subcategories.clear()
        self.cbx_subcategories.addItems(user_subcategory[0] for user_subcategory in self.subcategories)

    def set_transactions_model(self):
        self.transactions_list = self.presenter.get_transactions_list()
        self.transactions_list_model = TableModel(self.transactions_list)
        self.tbl_transactions.setModel(self.transactions_list_model)

    def clear_fields(self):
        # call on delete as well to reset
        self.on_transfer_account_toggle()
        self.tbl_transactions.clearSelection()
        self.current_value = None
        self.current_account_id = None
        self.transaction_type = None
        self.transaction_id = None
        self.cbx_account.setCurrentIndex(0)
        self.cbx_subcategories.setCurrentIndex(0)
        self.cbx_transaction_type.setCurrentIndex(0)
        self.cbx_target_account.clear()
        self.chk_transfer_account_toggle.setChecked(False)
        self.dte_transaction_date.setDate(QDate.currentDate())
        self.dsp_value.setValue(0)
        self.lne_description.setText("")
        self.btn_add_transaction.setText("Add transaction")
        self.btn_edit_transaction.setEnabled(False)
        self.btn_delete_transaction.setEnabled(False)
        self.btn_clear.setEnabled(False)

    def on_currency_change(self):
        self.dsp_value.setPrefix(f"{self.currency_list[self.cbx_currencies.currentText()].value} ")

    def on_subcategory_change(self):
        for user_subcategory in self.subcategories:
            if user_subcategory[0] == self.cbx_subcategories.currentText():
                currency_and_value = user_subcategory[1].split(" ")
                if currency_and_value[1] == "None":
                    self.dsp_recurring_value.setValue(0.00)
                else:
                    self.dsp_recurring_value.setPrefix(f"{currency_and_value[0]} ")
                    self.dsp_recurring_value.setValue(int(currency_and_value[1]) / 100)

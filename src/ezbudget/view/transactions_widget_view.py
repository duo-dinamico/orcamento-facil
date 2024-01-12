from PySide6.QtCore import QAbstractTableModel, QDate, QDateTime, QModelIndex, Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QDateEdit,
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
        self.headers = ["Account", "Category", "Date", "Value", "Description"]

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
            elif index.column() == 3:  # Value column
                return str(row_data.value)
            elif index.column() == 4:  # Description column
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
        self.cbx_target_account = QComboBox()
        self.cbx_subcategories = QComboBox()
        self.dte_transaction_date = QDateEdit()
        self.lne_value = QLineEdit()
        self.lne_description = QLineEdit()
        self.btn_add_transaction = QPushButton("Add transaction")
        self.btn_edit_transaction = QPushButton("Edit transaction")
        self.btn_delete_transaction = QPushButton("Delete transaction")
        self.btn_clear = QPushButton("Clear")
        self.tbl_transactions = QTableView()

        # setup the tables
        self.tbl_transactions.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tbl_transactions.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tbl_transactions.clicked.connect(self.on_table_view_selection)
        table_header = self.tbl_transactions.horizontalHeader()
        table_header.setSectionResizeMode(QHeaderView.Stretch)

        # get the data and set it to the models
        self.populate_target_accounts()
        self.populate_subcategories()
        self.set_transactions_model()

        # setup of calendar
        min_date = QDate(QDate.currentDate().year(), QDate.currentDate().month(), 1)
        max_date = QDate(QDate.currentDate().year(), QDate.currentDate().month(), min_date.daysInMonth())
        self.dte_transaction_date.setCalendarPopup(True)
        self.dte_transaction_date.setDisplayFormat("dd/MM/yyyy")
        self.dte_transaction_date.setDate(QDate.currentDate())
        self.dte_transaction_date.setDateRange(min_date, max_date)

        # setup the frame
        frm_add_edit_transactions.addRow("Account", self.cbx_target_account)
        frm_add_edit_transactions.addRow("Category", self.cbx_subcategories)
        frm_add_edit_transactions.addRow("Date", self.dte_transaction_date)
        frm_add_edit_transactions.addRow("Value", self.lne_value)
        frm_add_edit_transactions.addRow("Description", self.lne_description)

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
                self.transaction_id, self.get_transaction_data(), self.current_value, self.current_account_id
            )
        )
        self.btn_delete_transaction.clicked.connect(
            lambda: self.presenter.remove_transaction(self.get_transaction_data(), self.transaction_id)
        )
        self.btn_clear.clicked.connect(self.clear_fields)

        # setup the horizontal layouts
        hbl_transactions.addWidget(self.tbl_transactions, 2)
        hbl_transactions.addLayout(vbl_add_edit_transactions, 1)

        # chose the horizontal layout as the main one
        self.setLayout(hbl_transactions)

    def on_table_view_selection(self, index):
        selected_row = index.row()
        transaction = self.transactions_list[selected_row]
        selected_index = self.tbl_transactions.selectionModel().currentIndex()
        self.current_value = transaction.value
        self.current_account_id = transaction.account.id
        self.transaction_id = selected_index.siblingAtColumn(0).data(Qt.UserRole)
        self.cbx_target_account.setCurrentText(transaction.account.name)
        self.cbx_subcategories.setCurrentText(
            f"{transaction.subcategory.category.name} - {transaction.subcategory.name}"
        )
        self.dte_transaction_date.setDate(transaction.date)
        self.lne_value.setText(str(transaction.value))
        self.lne_description.setText(transaction.description)
        self.btn_add_transaction.setText("Duplicate transaction")
        self.btn_edit_transaction.setEnabled(True)
        self.btn_delete_transaction.setEnabled(True)
        self.btn_clear.setEnabled(True)

    def get_transaction_data(self):
        return {
            "account_name": self.cbx_target_account.currentText(),
            "subcategory_name": self.cbx_subcategories.currentText(),
            "date": self.dte_transaction_date.date().toString("yyyy/MM/dd"),
            "value": self.lne_value.text(),
            "description": self.lne_description.text(),
        }

    def populate_target_accounts(self):
        self.target_accounts = self.presenter.get_target_accounts()
        self.cbx_target_account.clear()
        self.cbx_target_account.addItems(self.target_accounts)

    def populate_subcategories(self):
        self.subcategories = self.presenter.get_user_subcategory_list()
        self.cbx_subcategories.clear()
        self.cbx_subcategories.addItems(self.subcategories)

    def set_transactions_model(self):
        self.transactions_list = self.presenter.get_transactions_list()
        self.transactions_list_model = TableModel(self.transactions_list)
        self.tbl_transactions.setModel(self.transactions_list_model)

    def clear_fields(self):
        ...

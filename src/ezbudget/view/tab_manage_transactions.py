from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
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

from ezbudget.view.models import TableModel, TransactionItem
from ezbudget.view.styles import DateSetup, DoubleSpinBox, MainTitle


class Transactions(QWidget):
    def __init__(self, parent, presenter):
        super().__init__()
        self.presenter = presenter
        self._parent = parent
        self.selection_index = None

        # instances of necessary widgets
        hbl_transactions = QHBoxLayout()
        vbl_add_edit_transactions = QVBoxLayout()
        vbl_main_layout = QVBoxLayout()
        frm_add_edit_transactions = QFormLayout()
        self.cbx_account = QComboBox()
        self.cbx_subcategories = QComboBox()
        self.cbx_currencies = QComboBox()
        self.cbx_transaction_type = QComboBox()
        self.cbx_target_account = QComboBox()
        self.chk_transfer_account_toggle = QCheckBox()
        self.lne_description = QLineEdit()
        self.btn_add_transaction = QPushButton("Add transaction")
        self.btn_edit_transaction = QPushButton("Edit transaction")
        self.btn_delete_transaction = QPushButton("Delete transaction")
        self.btn_clear = QPushButton("Clear")
        self.tbl_transactions = QTableView()
        grb_add_transaction = QGroupBox("Add/Edit/Remove transactions")

        # configure entries
        self.populate_currencies()
        self.cbx_currencies.currentTextChanged.connect(self.on_currency_change)

        lbl_title_transactions = MainTitle("Manage transactions")
        self.dte_transaction_date = DateSetup("dd/MM/yyyy", "current month")
        self.dsp_value = DoubleSpinBox(f"{self.currency_list[self.cbx_currencies.currentText()].value} ")
        self.dsp_recurring_value = DoubleSpinBox()
        self.dsp_recurring_value.setEnabled(False)

        # setup the model and set it to the table
        self.transactions_list = self.presenter.get_transactions_list()
        transaction_items = [TransactionItem(transaction) for transaction in self.transactions_list]
        self.transactions_list_model = TableModel(transaction_items)
        self.tbl_transactions.setModel(self.transactions_list_model)

        # setup the tables
        self.tbl_transactions.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tbl_transactions.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tbl_transactions.setAlternatingRowColors(True)
        self.tbl_transactions.clicked.connect(self.on_table_view_selection)
        table_header = self.tbl_transactions.horizontalHeader()
        table_header.setSectionResizeMode(QHeaderView.Stretch)

        # get the data and set it to the models
        self.populate_accounts()
        self.populate_subcategories()
        self.populate_transaction_types()
        self.on_subcategory_change()

        # target accounts setup
        self.cbx_target_account.setEnabled(False)
        self.cbx_account.currentTextChanged.connect(self.on_transfer_account_toggle)
        self.chk_transfer_account_toggle.stateChanged.connect(self.on_transfer_account_toggle)

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

        # setup the add / edit frame
        grb_add_transaction.setLayout(frm_add_edit_transactions)
        vbl_add_edit_transactions.addWidget(lbl_title_transactions)
        vbl_add_edit_transactions.addWidget(grb_add_transaction)
        vbl_add_edit_transactions.addSpacing(500)
        vbl_add_edit_transactions.addWidget(self.btn_add_transaction)
        vbl_add_edit_transactions.addWidget(self.btn_edit_transaction)
        vbl_add_edit_transactions.addWidget(self.btn_delete_transaction)
        vbl_add_edit_transactions.addWidget(self.btn_clear)
        vbl_add_edit_transactions.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.btn_edit_transaction.setEnabled(False)
        self.btn_delete_transaction.setEnabled(False)
        self.btn_clear.setEnabled(False)
        self.btn_add_transaction.clicked.connect(self.add_transaction)
        self.btn_edit_transaction.clicked.connect(self.update_transaction)
        self.btn_delete_transaction.clicked.connect(self.remove_transaction)
        self.btn_clear.clicked.connect(self.reset_fields)
        self.cbx_subcategories.currentTextChanged.connect(self.on_subcategory_change)

        # setup the horizontal layouts
        hbl_transactions.addLayout(vbl_add_edit_transactions, 1)
        hbl_transactions.addWidget(self.tbl_transactions, 2)

        # listen for an accounts signal
        self._parent.incoming_outgoing.account_list_model.rowsInserted.connect(self.populate_accounts)
        self._parent.manage_categories.user_subcategory_list_model.rowsInserted.connect(self.populate_subcategories)
        self.transactions_list_model.rowsInserted.connect(self.on_model_update)
        self.transactions_list_model.dataChanged.connect(self.on_model_update)
        self.transactions_list_model.rowsRemoved.connect(self.on_model_update)
        self.transactions_list_model.rowsInserted.connect(self.presenter.update_accounts_from_transaction)
        self.transactions_list_model.dataChanged.connect(self.presenter.update_accounts_from_transaction)
        self.transactions_list_model.rowsRemoved.connect(self.presenter.update_accounts_from_transaction)

        # setup everything on the main layout
        vbl_main_layout.addLayout(hbl_transactions)

        # chose the horizontal layout as the main one
        self.setLayout(vbl_main_layout)

    def populate_currencies(self):
        self.currency_list = self.presenter.get_currency()
        self.cbx_currencies.clear()
        self.cbx_currencies.addItems([currency.name for currency in self.currency_list])

    def populate_transaction_types(self):
        self.transaction_types_list = self.presenter.get_transaction_types()
        self.cbx_transaction_type.clear()
        self.cbx_transaction_type.addItems([transaction_type.name for transaction_type in self.transaction_types_list])

    def set_data_on_selection(self, transaction_item):
        self.cbx_account.setCurrentText(transaction_item.account_name)
        if transaction_item.transactionTypeName() == "Transfer":
            self.chk_transfer_account_toggle.setChecked(True)
            target_account_name = self.presenter.get_account_by_id(transaction_item.target_account_id).name
            self.cbx_target_account.setCurrentText(target_account_name)
        else:
            self.chk_transfer_account_toggle.setChecked(False)
        self.cbx_subcategories.setCurrentText(transaction_item.category())
        self.dte_transaction_date.setDate(transaction_item._date)
        self.cbx_currencies.setCurrentText(transaction_item.currencyName())
        self.cbx_transaction_type.setCurrentText(transaction_item.transactionTypeName())
        self.dsp_value.setValue(transaction_item.value())
        self.lne_description.setText(transaction_item.description)

    def get_selected_item(self):
        return self.selection_index.internalPointer()

    def on_table_view_selection(self, index):
        self.selection_index = index
        item = self.get_selected_item()
        self.set_data_on_selection(item)
        self.btn_add_transaction.setText("Duplicate transaction")
        self.btn_edit_transaction.setEnabled(True)
        self.btn_delete_transaction.setEnabled(True)
        self.btn_clear.setEnabled(True)

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

    def add_transaction(self):
        transaction_data = self.get_transaction_data()
        new_transaction = self.presenter.create_transaction(transaction_data)
        if isinstance(new_transaction, str):
            # TODO add a label for the message error
            print(new_transaction)
        else:
            self.transactions_list_model.addTransaction(TransactionItem(new_transaction))

    def update_transaction(self):
        item = self.get_selected_item()
        transaction_data = self.get_transaction_data()
        updated_transaction_data = self.presenter.update_transaction(item, transaction_data)
        updated_transaction_item = TransactionItem(updated_transaction_data)
        self.transactions_list_model.updateTransaction(item, updated_transaction_item)

    def remove_transaction(self):
        item = self.get_selected_item()
        # TODO add a label for the message error
        self.presenter.remove_transaction(item)
        self.transactions_list_model.removeTransaction(item)

    def populate_accounts(self):
        self.accounts: list = self.presenter.get_accounts()
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
        if self.subcategories is None:
            self.subcategories = []
        self.on_subcategory_change()
        self.cbx_subcategories.clear()
        self.cbx_subcategories.addItems(
            f"{user_subcategory.subcategory.category.name} - {user_subcategory.subcategory.name}"
            for user_subcategory in self.subcategories
        )

    def reset_fields(self):
        self.tbl_transactions.clearSelection()
        self.selection_index = None

        self.cbx_account.setCurrentIndex(0)
        self.chk_transfer_account_toggle.setChecked(False)
        self.on_transfer_account_toggle()
        self.cbx_subcategories.setCurrentIndex(0)
        self.dte_transaction_date.setDate(QDate.currentDate())
        self.cbx_currencies.setCurrentIndex(0)
        self.cbx_transaction_type.setCurrentIndex(0)
        self.dsp_value.setValue(0.00)
        self.lne_description.setText("")

        self.btn_add_transaction.setText("Add transaction")
        self.btn_edit_transaction.setEnabled(False)
        self.btn_delete_transaction.setEnabled(False)
        self.btn_clear.setEnabled(False)

    def on_currency_change(self):
        self.dsp_value.setPrefix(f"{self.currency_list[self.cbx_currencies.currentText()].value} ")

    def on_subcategory_change(self):
        for user_subcategory in self.subcategories:
            user_category_name = f"{user_subcategory.subcategory.category.name} - {user_subcategory.subcategory.name}"
            if user_category_name == self.cbx_subcategories.currentText():
                currency_and_value = f"{user_subcategory.subcategory.currency.value if user_subcategory.subcategory.currency is not None else None} {user_subcategory.subcategory.recurrence_value}".split(
                    " "
                )
                if currency_and_value[1] == "None":
                    self.dsp_recurring_value.setValue(0.00)
                else:
                    self.dsp_recurring_value.setPrefix(f"{currency_and_value[0]} ")
                    self.dsp_recurring_value.setValue(int(currency_and_value[1]) / 100)

    def on_model_update(self):
        self.reset_fields()

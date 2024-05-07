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

from ezbudget.view.models import CurrencyItem
from ezbudget.view.styles import (
    DateSetup,
    DoubleSpinBox,
    ErrorMessage,
    MadatoryFields,
    MainTitle,
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
        formatted_data = []
        for data in data_list:
            currency_amount = data.balance / 100
            currency_with_value = CurrencyItem(data.currency, currency_amount)
            formatted_data.append((data.name, currency_with_value.valueWithCurrency()))
        self._data = formatted_data
        self.endResetModel()


class IncomeSources(QWidget):
    def __init__(self, parent, presenter):
        super().__init__()
        self.presenter = presenter
        self._parent = parent

        # instances of necessary widgets
        vbl_main_layout = QVBoxLayout()
        vbl_income_sources_controls = QVBoxLayout()
        hbl_income_sources = QHBoxLayout()
        frm_add_edit_incomings = QFormLayout()
        grb_incomings_controls = QGroupBox("Manage income sources")
        self.lne_incoming_name = QLineEdit()
        self.lne_incoming_real = QLineEdit()
        self.cbx_incoming_account = QComboBox()
        self.cbx_incoming_currency = QComboBox()
        self.cbx_incoming_recurrence = QComboBox()
        self.cbx_incoming_recurrent = QComboBox()
        self.btn_incoming_add = QPushButton("Add income source")
        btn_incoming_edit = QPushButton("Edit income source")
        btn_incoming_delete = QPushButton("Delete incoime source")
        self.tbl_incomings = QTableView()

        self.clear_timer = None
        lbl_incomes_title = MainTitle("Income sources")
        self.lbl_income_error_message = ErrorMessage("")
        lbl_income_mandatory_fields = MadatoryFields("Fields with an asterisk (*) are mandatory")
        self.dsp_incoming_expected = DoubleSpinBox()
        self.dte_incoming_date = DateSetup("dd/MM", "yearly")

        # setup and link models to tables
        self.incoming_list = self.presenter.get_income_list()
        incoming_list_data = self.format_model_data(self.incoming_list)
        self.incoming_list_model = TableModel(
            incoming_list_data,
            ["Name", "Expected Income"],
            self.presenter.get_income_list,
        )
        self.tbl_incomings.setModel(self.incoming_list_model)

        self.starting_setup()

        # setup combobox and buttons
        btn_incoming_edit.setEnabled(False)
        btn_incoming_delete.setEnabled(False)
        self.btn_incoming_add.clicked.connect(self.create_income_source)

        # organize the buttons into the controls layout
        income_sources_controls = [self.btn_incoming_add, btn_incoming_edit, btn_incoming_delete]
        vbl_income_sources_controls.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        for btn in income_sources_controls:
            vbl_income_sources_controls.addWidget(btn)

        # configure entries
        self.lne_incoming_name.setPlaceholderText("Enter income name...")
        self.cbx_incoming_currency.currentTextChanged.connect(self.on_income_currency_change)

        # add entries to form layouts
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

        # setup the tables
        self.tbl_incomings.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tbl_incomings.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tbl_incomings.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tbl_incomings.setAlternatingRowColors(True)
        self.tbl_incomings.clicked.connect(self.on_incoming_table_view_selection)

        # signals from the models to update other elements
        self.incoming_list_model.rowsInserted.connect(self.on_model_row_inserted)

        # setup the vertical layouts
        grb_incomings_controls.setLayout(vbl_income_sources_controls)

        # setup the controls widgets
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
                vbl_income_sources_controls.addLayout(widget)
            else:
                vbl_income_sources_controls.addWidget(widget)

        # setup the vertical layouts inside the horizontal layout
        hbl_income_sources.addWidget(self.tbl_incomings, 2)
        hbl_income_sources.addWidget(grb_incomings_controls, 1)

        # setup everything on the main layout
        vbl_main_layout.addWidget(lbl_incomes_title)
        vbl_main_layout.addLayout(hbl_income_sources)

        # chose the horizontal layout as the main one
        self.setLayout(vbl_main_layout)

        # listen for an accounts signal
        self._parent.accounts.account_list_model.rowsInserted.connect(self.populate_target_accounts)

    def starting_setup(self):
        self.populate_currencies()
        self.populate_target_accounts()
        self.populate_recurrence()
        self.on_income_currency_change()

    def get_income_source_data(self):
        return {
            "name": self.lne_incoming_name.text(),
            "account_name": self.cbx_incoming_account.currentText(),
            "recurrence_value": self.dsp_incoming_expected.value() * 100,
            "income_date": self.dte_incoming_date.date().toString("yyyy/MM/dd"),
            "currency_id": self.selected_income_currency.getId(),
            "recurrent": True if self.cbx_incoming_recurrent.currentText() == "Yes" else False,
            "recurrence": (
                self.cbx_incoming_recurrence.currentText()
                if self.cbx_incoming_recurrent.currentText() == "Yes"
                else None
            ),
        }

    def create_income_source(self):
        data = self.get_income_source_data()
        new_income_source = self.presenter.create_income(data)
        if isinstance(new_income_source, str):
            self.set_error_message(new_income_source)
        else:
            currency_amount = new_income_source.recurrence_value / 100
            currency_with_value = CurrencyItem(new_income_source.currency, currency_amount)
            self.incoming_list.append(new_income_source)
            self.incoming_list_model.addData(
                [
                    new_income_source.name,
                    currency_with_value.valueWithCurrency(),
                ]
            )

    def on_incoming_table_view_selection(self, index):
        selected_row = index.row()
        income_source = self.incoming_list[selected_row]
        self.lne_incoming_name.setText(income_source.name)
        self.cbx_incoming_account.setCurrentText(income_source.account.name)
        self.dsp_incoming_expected.setValue(income_source.recurrence_value / 100)
        self.dte_incoming_date.setDate(income_source.income_date)
        self.cbx_incoming_currency.setCurrentText(income_source.currency.name)
        self.cbx_incoming_recurrence.setCurrentText(income_source.recurrence.value)

    def on_recurrent_change(self):
        if self.cbx_incoming_recurrent.currentText() == "No":
            self.cbx_incoming_recurrence.setDisabled(True)
        else:
            self.cbx_incoming_recurrence.setDisabled(False)

    def set_error_message(self, message: str) -> None:
        self.lbl_income_error_message.setText(message)
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
        self.lbl_income_error_message.clear()
        # Stop the timer after clearing the messages
        if self.clear_timer:
            self.clear_timer.stop()

    def on_income_currency_change(self):
        current_incoming_currency = self.cbx_incoming_currency.currentText()
        for currency in self.currency_list:
            if currency.getName() == current_incoming_currency:
                self.selected_income_currency = currency
                self.dsp_incoming_expected.setPrefix(currency.getSymbol())

    def clear_income_data(self):
        self.lne_incoming_name.clear()
        self.cbx_incoming_account.setCurrentIndex(0)
        self.cbx_incoming_currency.setCurrentIndex(0)
        self.dsp_incoming_expected.setValue(0.00)
        self.dte_incoming_date.clear()
        self.cbx_incoming_recurrence.setCurrentIndex(0)

    def on_model_row_inserted(self):
        self.clear_income_data()

    def populate_currencies(self):
        all_currencies = self.presenter.get_currency()
        self.currency_list = [CurrencyItem(currency) for currency in all_currencies]
        self.cbx_incoming_currency.clear()
        self.cbx_incoming_currency.addItems([currency.getName() for currency in self.currency_list])

    def populate_target_accounts(self):
        accounts: list = self.presenter.get_accounts()
        if len(accounts) > 0:
            self.btn_incoming_add.setEnabled(True)
        else:
            self.btn_incoming_add.setEnabled(False)
        self.cbx_incoming_account.clear()
        self.cbx_incoming_account.addItems(accounts)

    def populate_recurrence(self):
        self.recurrence_list = self.presenter.get_recurrence()
        self.cbx_incoming_recurrence.clear()
        self.cbx_incoming_recurrence.addItems([recurrence.value for recurrence in self.recurrence_list])

    def format_model_data(self, data_list: list) -> list:
        response = []
        for data in data_list:
            currency_with_value = CurrencyItem(data.currency, data.recurrence_value / 100)
            response.append((data.name, currency_with_value.valueWithCurrency()))
        return response

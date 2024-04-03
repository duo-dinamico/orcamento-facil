from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLineEdit,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from ezbudget.view.styles import MainTitle


class SummaryModel(QAbstractTableModel):
    def __init__(self, summaries):
        super().__init__()
        self.summaries = summaries
        self.headers = [
            "Category",
            "Anual budget",
            "Recurrent value",
            "Recurrence",
            "Current month value",
            "Difference",
        ]

    def rowCount(self, parent=QModelIndex()):
        return len(self.summaries)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(self.summaries[index.row()][index.column()])

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]


class MonthlyBudget(QWidget):
    def __init__(self, presenter):
        super().__init__()
        self.presenter = presenter

        # setup layouts
        vbl_summary_layout = QVBoxLayout()
        hbl_top_layout = QHBoxLayout()
        hbl_bottom_layout = QHBoxLayout()
        frm_income_summary = QFormLayout()
        frm_expenses_summary = QFormLayout()

        # setup other widgets
        grb_income_summary = QGroupBox("Income Summary")
        grb_expenses_summary = QGroupBox("Expenses Summary")
        self.lne_budgeted_income = QLineEdit()
        self.lne_budgeted_expenses = QLineEdit()
        self.lne_month_income = QLineEdit()
        self.lne_month_expenses = QLineEdit()
        self.tbl_summary = QTableView()

        lbl_account_summary = MainTitle("Monthly Budget")

        # setup line edits
        self.lne_budgeted_income.setReadOnly(True)
        self.lne_budgeted_expenses.setReadOnly(True)
        self.lne_month_income.setReadOnly(True)
        self.lne_month_expenses.setReadOnly(True)

        # add rows to form layout
        frm_income_summary.addRow("Monthly income", self.lne_month_income)
        frm_income_summary.addRow("Budgeted income", self.lne_budgeted_income)
        frm_expenses_summary.addRow("Monthly expenses", self.lne_month_expenses)
        frm_expenses_summary.addRow("Budgeted expenses", self.lne_budgeted_expenses)

        # setup the tables
        self.tbl_summary.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tbl_summary.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tbl_summary.clicked.connect(self.on_table_selection)
        table_header = self.tbl_summary.horizontalHeader()
        table_header.setSectionResizeMode(QHeaderView.Stretch)

        # arrange layouts
        grb_income_summary.setLayout(frm_income_summary)
        grb_expenses_summary.setLayout(frm_expenses_summary)
        vbl_summary_layout.addLayout(hbl_top_layout, 1)
        vbl_summary_layout.addLayout(hbl_bottom_layout, 4)
        hbl_top_layout.addWidget(lbl_account_summary, 1)
        hbl_top_layout.addWidget(grb_income_summary, 1)
        hbl_top_layout.addWidget(grb_expenses_summary, 1)
        hbl_bottom_layout.addWidget(self.tbl_summary, 1)

        # load methods to populate
        self.total_budgeted()
        self.set_table_selection()

        # set main layout
        self.setLayout(vbl_summary_layout)

    def total_budgeted(self):
        total_budgeted = self.presenter.get_total_budgeted()
        total = self.presenter.get_total_real()
        self.lne_budgeted_income.setText(f'{total_budgeted["budgeted_income"] / 100}')
        self.lne_budgeted_expenses.setText(f'{total_budgeted["budgeted_expenses"] / 100}')
        self.lne_month_income.setText(f'{total["total_income"] / 100}')
        self.lne_month_expenses.setText(f'{total["total_expenses"] / 100}')

    def on_table_selection(self):
        ...

    def set_table_selection(self):
        self.summary = self.presenter.get_month_summary()
        self.summary_model = SummaryModel(self.summary)
        self.tbl_summary.setModel(self.summary_model)

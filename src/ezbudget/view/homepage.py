from PySide6.QtWidgets import QTabWidget, QVBoxLayout, QWidget

from ezbudget.view import (
    Accounts,
    Categories,
    HeaderView,
    IncomeSources,
    MonthlyBudget,
    Summary,
    Transactions,
)


class HomePageView(QWidget):
    def __init__(self, presenter, user):
        super().__init__()
        self.presenter = presenter
        self.user = user

        # attributes
        self.header = HeaderView(self.presenter, self.user)

        # setup the layout
        vbl_homepage = QVBoxLayout()

        # setup table view for accounts
        self.summary = Summary(self.presenter)
        self.accounts = Accounts(self, self.presenter)
        self.income_sources = IncomeSources(self, self.presenter)
        self.categories = Categories(self.presenter)
        self.transactions = Transactions(self, self.presenter)
        self.monthly_budget = MonthlyBudget(self.presenter)

        # setup the stacked layout
        tbl_homepage = QTabWidget()
        tbl_homepage.setTabPosition(QTabWidget.South)
        tbl_homepage.addTab(self.summary, "Home")
        tbl_homepage.addTab(self.accounts, "Accounts")
        tbl_homepage.addTab(self.income_sources, "Income Sources")
        tbl_homepage.addTab(self.categories, "Categories")
        tbl_homepage.addTab(self.transactions, "Transactions")
        tbl_homepage.addTab(self.monthly_budget, "Monthly Budget")

        # place the widgets
        vbl_homepage.addWidget(self.header, 1)
        vbl_homepage.addWidget(tbl_homepage, 15)

        # set the base layout
        self.setLayout(vbl_homepage)

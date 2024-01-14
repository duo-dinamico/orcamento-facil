from PySide6.QtWidgets import QTabWidget, QVBoxLayout, QWidget

from ezbudget.view import Categories, HeaderView, IncomingOutgoing, Transactions


class HomePageView(QWidget):
    def __init__(self, presenter, user):
        super().__init__()
        self.presenter = presenter
        self.user = user

        # attributes
        self.header = HeaderView(self.user)

        # setup the layout
        vbl_homepage = QVBoxLayout()

        # setup table view for accounts
        self.incoming_outgoing = IncomingOutgoing(self.presenter)
        self.manage_categories = Categories(self.presenter)
        self.transactions = Transactions(self.presenter)

        # setup the stacked layout
        tbl_homepage = QTabWidget()
        tbl_homepage.setTabPosition(QTabWidget.South)
        tbl_homepage.addTab(QWidget(), "Home")
        tbl_homepage.addTab(self.incoming_outgoing, "Manage Accounts")
        tbl_homepage.addTab(self.manage_categories, "Manage Categories")
        tbl_homepage.addTab(self.transactions, "Manage Transactions")

        # place the widgets
        vbl_homepage.addWidget(self.header, 1)
        vbl_homepage.addWidget(tbl_homepage, 15)

        # set the base layout
        self.setLayout(vbl_homepage)

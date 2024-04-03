from PySide6.QtWidgets import QHBoxLayout, QWidget

from ezbudget.view.styles import MainTitle


class Summary(QWidget):
    def __init__(self, presenter):
        super().__init__()
        self.presenter = presenter

        # setup widgets
        hbl_summary_layout = QHBoxLayout()
        lbl_account_summary = MainTitle("Summary of all accounts")

        hbl_summary_layout.addWidget(lbl_account_summary)

        self.setLayout(hbl_summary_layout)

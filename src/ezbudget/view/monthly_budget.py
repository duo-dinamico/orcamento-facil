from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget


class MonthlyBudget(QWidget):
    def __init__(self, presenter):
        super().__init__()
        self.presenter = presenter

        # setup widgets
        hbl_summary_layout = QHBoxLayout()
        lbl_account_summary = QLabel("Monthly Budget")

        # welcome font setup
        fnt_summary_title = lbl_account_summary.font()
        fnt_summary_title.setPointSize(24)
        fnt_summary_title.setBold(True)
        lbl_account_summary.setFont(fnt_summary_title)
        lbl_account_summary.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        hbl_summary_layout.addWidget(lbl_account_summary)

        self.setLayout(hbl_summary_layout)

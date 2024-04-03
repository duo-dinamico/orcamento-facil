from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import QDateEdit, QDoubleSpinBox

MINIMUM = -999999.99
MAXIMUM = 999999.99
CURRENT_YEAR = QDate.currentDate().year()
CURRENT_MONTH = QDate.currentDate().month()


class DoubleSpinBox(QDoubleSpinBox):
    def __init__(self, prefix: str = None) -> None:
        super().__init__()
        self.setRange(MINIMUM, MAXIMUM)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setPrefix(prefix)


class DateSetup(QDateEdit):
    def __init__(self, display_format: str, timerange: str) -> None:
        super().__init__()
        if timerange == "yearly":
            min_date = QDate(CURRENT_YEAR, 1, 1)
            max_date = QDate(CURRENT_YEAR, 12, 31)
        if timerange == "current month":
            min_date = QDate(CURRENT_YEAR, CURRENT_MONTH, 1)
            max_date = QDate(CURRENT_YEAR, CURRENT_MONTH, min_date.daysInMonth())
        self.setCalendarPopup(True)
        self.setDisplayFormat(display_format)
        self.setDate(QDate.currentDate())
        self.setDateRange(min_date, max_date)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

MAIN_TITLE_FONT_SIZE = 18
SECONDARY_TITLE_FONT_SIZE = 14
ERROR_MESSAGE_FONT_SIZE = 12
ALIGNMENT_H_CENTER = Qt.AlignmentFlag.AlignHCenter
ALIGNMENT_TOP = Qt.AlignmentFlag.AlignTop
ALIGNMENT_BOTTOM = Qt.AlignmentFlag.AlignBottom
ALIGNMENT_LEFT = Qt.AlignmentFlag.AlignLeft


class MainTitle(QLabel):
    def __init__(self, title: str) -> None:
        super().__init__(title)
        self._font = self.font()
        self._font.setPointSize(MAIN_TITLE_FONT_SIZE)
        self._font.setBold(True)
        self.setFont(self._font)
        if title == "Welcome!":
            self.setAlignment(ALIGNMENT_H_CENTER | ALIGNMENT_TOP)
        else:
            self.setAlignment(ALIGNMENT_LEFT | ALIGNMENT_TOP)


class SecondaryTitle(QLabel):
    def __init__(self, title: str) -> None:
        super().__init__(title)
        self._font = self.font()
        self._font.setPointSize(SECONDARY_TITLE_FONT_SIZE)
        self._font.setBold(True)
        self.setFont(self._font)


class ErrorMessage(QLabel):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self._font = self.font()
        self._font.setPointSize(ERROR_MESSAGE_FONT_SIZE)
        self._font.setBold(True)
        self.setWordWrap(True)
        self.setStyleSheet("color: rgb(250,0,0)")
        self.setAlignment(ALIGNMENT_H_CENTER | ALIGNMENT_BOTTOM)


class MadatoryFields(QLabel):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self._font = self.font()
        self._font.setBold(True)
        self.setStyleSheet("color: rgb(250,0,0)")
        self.setAlignment(ALIGNMENT_LEFT | ALIGNMENT_TOP)

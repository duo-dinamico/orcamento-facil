from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QListView,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ezbudget.model import CategoryTypeEnum
from ezbudget.view.models import AbstractListModel, CurrencyItem, SubCategoryItem
from ezbudget.view.styles import DoubleSpinBox, ErrorMessage, MainTitle


class Categories(QWidget):
    def __init__(self, presenter):
        super().__init__()
        self.presenter = presenter

        # instances of necessary widgets
        vbl_main_layout = QVBoxLayout()
        vbl_categories = QVBoxLayout()
        vbl_subcategories = QVBoxLayout()
        hbl_user_categories = QHBoxLayout()
        grb_categories = QGroupBox("Manage Categories")
        grb_subcategories = QGroupBox("Manage Sub Categories")
        self.cbx_categories = QComboBox()
        self.cbx_edit_category_types = QComboBox()
        self.cbx_add_category_types = QComboBox()
        self.cbx_currencies = QComboBox()
        self.cbx_recurrent = QComboBox()
        self.cbx_recurrence = QComboBox()
        frm_manage_categories = QFormLayout()
        frm_add_category = QFormLayout()
        frm_edit_subcategories = QFormLayout()
        self.lne_edit_category_name = QLineEdit()
        self.lne_add_category_name = QLineEdit()
        self.lne_subcategory_name = QLineEdit()
        btn_add_category = QPushButton("Add Category")
        btn_save_category = QPushButton("Save Changes")
        btn_delete_category = QPushButton("Delete Category")
        btn_add_subcategory = QPushButton("Add Subcategory")
        self.btn_save_subcategory = QPushButton("Save Changes")
        self.btn_delete_subcategory = QPushButton("Delete Subcategory")
        self.lvw_user_categories = QListView(self)

        self.populate_currencies()

        # widgets with styles
        self.clear_timer = None
        lbl_title_manage_categories = MainTitle("Manage Categories")
        self.lbl_category_error_message = ErrorMessage("")
        self.lbl_add_category_error_message = ErrorMessage("")
        self.lbl_subcategory_error_message = ErrorMessage("")
        current_currency = self.cbx_currencies.currentText()
        for currency in self.currency_list:
            if currency.getName() == current_currency:
                self.dsp_value = DoubleSpinBox(currency.getSymbol())

        # setup subcategories model
        self.subcategories_model = AbstractListModel()
        self.lvw_user_categories.setModel(self.subcategories_model)

        # setup form
        frm_manage_categories.addRow("Name", self.lne_edit_category_name)
        frm_manage_categories.addRow("Type", self.cbx_edit_category_types)
        frm_add_category.addRow("Name", self.lne_add_category_name)
        frm_add_category.addRow("Type", self.cbx_add_category_types)
        frm_edit_subcategories.addRow("Name", self.lne_subcategory_name)
        frm_edit_subcategories.addRow("Currency", self.cbx_currencies)
        frm_edit_subcategories.addRow("Recurrence value", self.dsp_value)
        frm_edit_subcategories.addRow("Recurrent", self.cbx_recurrent)
        self.cbx_recurrent.addItems(["Yes", "No"])
        self.cbx_recurrent.currentIndexChanged.connect(self.on_recurrent_change)
        frm_edit_subcategories.addRow("Recurrence", self.cbx_recurrence)

        # setup categories layout
        vbl_categories.addWidget(self.cbx_categories)
        vbl_categories.addLayout(frm_manage_categories)
        vbl_categories.addWidget(self.lbl_category_error_message)
        vbl_categories.addWidget(btn_save_category)
        vbl_categories.addWidget(btn_delete_category)
        vbl_categories.insertStretch(5, 1)
        vbl_categories.addLayout(frm_add_category)
        vbl_categories.addWidget(self.lbl_add_category_error_message)
        vbl_categories.addWidget(btn_add_category)

        # setup subcategories layout
        vbl_subcategories.addWidget(self.lvw_user_categories)
        vbl_subcategories.addLayout(frm_edit_subcategories)
        vbl_subcategories.addWidget(self.lbl_subcategory_error_message)
        vbl_subcategories.addWidget(btn_add_subcategory)
        vbl_subcategories.addWidget(self.btn_save_subcategory)
        vbl_subcategories.addWidget(self.btn_delete_subcategory)

        # place widgets
        grb_categories.setLayout(vbl_categories)
        grb_subcategories.setLayout(vbl_subcategories)
        hbl_user_categories.addWidget(grb_categories, 1)
        hbl_user_categories.addWidget(grb_subcategories, 1)
        vbl_main_layout.addWidget(lbl_title_manage_categories)
        vbl_main_layout.addLayout(hbl_user_categories, 1)

        # signals and slots
        self.cbx_categories.currentTextChanged.connect(self.on_category_change)
        btn_save_category.clicked.connect(self.on_save_category)
        btn_delete_category.clicked.connect(self.on_delete_category)
        btn_add_category.clicked.connect(self.on_add_category)
        self.cbx_currencies.currentTextChanged.connect(self.on_currency_change)
        btn_add_subcategory.clicked.connect(self.add_subcategory)
        self.btn_save_subcategory.setEnabled(False)
        self.btn_delete_subcategory.setEnabled(False)
        self.btn_delete_subcategory.clicked.connect(self.delete_subcategory)
        self.btn_save_subcategory.clicked.connect(self.update_subcategory)
        self.lvw_user_categories.clicked.connect(self.on_table_view_selection)
        self.subcategories_model.modelReset.connect(self.on_data_change)

        # initial setup
        self.starting_setup()

        # chose the horizontal layout as the main one
        self.setLayout(vbl_main_layout)

    def fetch_categories(self):
        self.category_list = self.presenter.get_category_list()
        self.cbx_categories.clear()
        self.cbx_categories.addItems([category.name for category in self.category_list])
        self.cbx_edit_category_types.clear()
        self.cbx_add_category_types.clear()
        self.cbx_edit_category_types.addItems([e.value for e in CategoryTypeEnum])
        self.cbx_add_category_types.addItems([e.value for e in CategoryTypeEnum])

    def fetch_subcategories(self):
        self.subcategory_list = self.presenter.get_subcategory_list()

    def populate_currencies(self):
        all_currencies = self.presenter.get_currency()
        self.currency_list = [CurrencyItem(currency) for currency in all_currencies]
        self.cbx_currencies.clear()
        self.cbx_currencies.addItems([currency.getName() for currency in self.currency_list])

    def on_currency_change(self):
        current_incoming_currency = self.cbx_currencies.currentText()
        for currency in self.currency_list:
            if currency.getName() == current_incoming_currency:
                self.selected_currency = currency
                self.dsp_value.setPrefix(currency.getSymbol())

    def populate_recurrence(self):
        self.recurrence_list = self.presenter.get_recurrence()
        self.cbx_recurrence.clear()
        self.cbx_recurrence.addItems([recurrence.value for recurrence in self.recurrence_list])

    def on_recurrent_change(self):
        if self.cbx_recurrent.currentText() == "No":
            self.cbx_recurrence.setDisabled(True)
        else:
            self.cbx_recurrence.setDisabled(False)

    def starting_setup(self):
        self.fetch_subcategories()
        self.fetch_categories()
        self.populate_currencies()
        self.populate_recurrence()
        self.on_category_change()
        self.refresh_model_data()

    def refresh_model_data(self):
        current_category_subcategories: list = []
        for subcategory in self.subcategory_list:
            if subcategory.category.name == self.current_category_name:
                subcategory_item = SubCategoryItem(subcategory)
                current_category_subcategories.append(subcategory_item)
        self.subcategories_model.setObjects(current_category_subcategories)

    def on_category_change(self):
        self.lne_edit_category_name.setText(self.cbx_categories.currentText())
        for category in self.category_list:
            if category.name == self.cbx_categories.currentText():
                self.current_category_id = category.id
                self.current_category_name = category.name
                self.current_category_type = category.category_type.value
        self.cbx_edit_category_types.setCurrentText(self.current_category_type)
        self.refresh_model_data()

    def get_category_data(self):
        return {"name": self.lne_edit_category_name.text(), "category_type": self.cbx_edit_category_types.currentText()}

    def get_add_category_data(self):
        return {"name": self.lne_add_category_name.text(), "category_type": self.cbx_add_category_types.currentText()}

    def get_subcategory_data(self):
        return {
            "category_name": self.cbx_categories.currentText(),
            "name": self.lne_subcategory_name.text(),
            "recurrent": True if self.cbx_recurrent.currentText() == "Yes" else False,
            "recurrence": self.cbx_recurrence.currentText() if self.cbx_recurrent.currentText() == "Yes" else None,
            "recurrence_value": self.dsp_value.value() * 100,
            "currency_id": self.selected_currency.getId(),
        }

    def on_save_category(self):
        response = self.presenter.update_category(self.current_category_id, self.get_category_data())
        if isinstance(response, str):
            self.set_error_message(response, "edit")
        else:
            self.fetch_categories()

    def on_delete_category(self):
        response = self.presenter.delete_category(self.current_category_id)
        if isinstance(response, str):
            self.set_error_message(response, "edit")
        else:
            self.fetch_categories()

    def set_error_message(self, message: str, type: str) -> None:
        if type == "edit":
            self.lbl_category_error_message.setText(message)
        elif type == "add":
            self.lbl_add_category_error_message.setText(message)
        elif type == "subcategory":
            self.lbl_subcategory_error_message.setText(message)
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
        self.lbl_category_error_message.setText("")
        self.lbl_subcategory_error_message.setText("")
        # Stop the timer after clearing the messages
        if self.clear_timer:
            self.clear_timer.stop()

    def on_add_category(self):
        response = self.presenter.create_category(self.get_add_category_data())
        if isinstance(response, str):
            self.set_error_message(response, "add")
        else:
            self.fetch_categories()
            self.clear_category_data()

    def add_subcategory(self):
        data = self.get_subcategory_data()
        new_subcategory = self.presenter.create_subcategory(data)
        if isinstance(new_subcategory, str):
            self.set_error_message(new_subcategory, "subcategory")
        else:
            self.fetch_subcategories()
            new_subcategory_item = SubCategoryItem(new_subcategory)
            self.subcategories_model.addListItem(new_subcategory_item)
            self.clear_subcategory_data()

    def on_table_view_selection(self, index):
        self.selection_index = index
        item: SubCategoryItem = self.get_selected_item()
        self.lne_subcategory_name.setText(item.getName())
        if item.getCurrencyName() is not None:
            self.cbx_currencies.setCurrentText(item.getCurrencyName())
        self.dsp_value.setValue(item.getValue())
        self.cbx_recurrent.setCurrentText("Yes") if item.recurrent is True else self.cbx_recurrent.setCurrentText("No"),
        if item.recurrent is True:
            self.cbx_recurrence.setCurrentText(item.recurrence.value)
        else:
            self.cbx_recurrence.setEnabled(False)
        self.btn_save_subcategory.setEnabled(True)
        self.btn_delete_subcategory.setEnabled(True)

    def on_data_change(self):
        self.selection_index = None
        self.btn_save_subcategory.setEnabled(False)
        self.btn_delete_subcategory.setEnabled(False)

    def get_selected_item(self):
        return self.selection_index.internalPointer()

    def update_subcategory(self):
        item: SubCategoryItem = self.get_selected_item()
        response = self.presenter.update_subcategory(item.getId(), self.get_subcategory_data())
        if isinstance(response, str):
            self.set_error_message(response, "subcategory")
        else:
            self.fetch_subcategories()
            self.refresh_model_data()
            self.clear_subcategory_data()

    def delete_subcategory(self):
        item: SubCategoryItem = self.get_selected_item()
        response = self.presenter.delete_subcategory(item.getId())
        if isinstance(response, str):
            self.set_error_message(response, "subcategory")
        else:
            self.fetch_subcategories()
            self.subcategories_model.removeListItem(self.selection_index)
            self.clear_subcategory_data()

    def clear_category_data(self):
        self.lne_add_category_name.clear()
        self.cbx_add_category_types.setCurrentIndex(0)

    def clear_subcategory_data(self):
        self.lne_subcategory_name.clear()
        self.cbx_recurrent.setCurrentIndex(0)
        self.cbx_recurrence.setCurrentIndex(0)
        self.dsp_value.setValue(0.00)
        self.cbx_currencies.setCurrentIndex(0)

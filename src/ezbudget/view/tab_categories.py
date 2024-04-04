from PySide6.QtCore import QItemSelectionModel, QModelIndex, QTimer
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QListView,
    QPushButton,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

from ezbudget.view.models import (
    CategoryItem,
    CategoryListModel,
    CategoryModel,
    CurrencyItem,
    UserCategoryItem,
)
from ezbudget.view.styles import DoubleSpinBox, ErrorMessage, MainTitle, SecondaryTitle


class Categories(QWidget):
    def __init__(self, presenter):
        super().__init__()
        self.presenter = presenter
        self.clear_timer = None

        # instances of necessary widgets
        hbl_manage_categories = QHBoxLayout()
        hbl_add_categories = QHBoxLayout()
        vbl_main_layout = QVBoxLayout()
        vbl_controls = QVBoxLayout()
        vbl_categories = QVBoxLayout()
        vbl_add_categories = QVBoxLayout()
        vbl_add_subcategories = QVBoxLayout()
        vbl_user_subcategories = QVBoxLayout()
        btn_select_users_categories = QPushButton(">>")
        btn_remove_users_categories = QPushButton("<<")
        btn_add_category = QPushButton("Add category")
        btn_add_subcategory = QPushButton("Add sub-category")
        self.lvw_user_categories = QListView(self)
        grb_add_categories = QGroupBox("Add Categories")
        grb_add_subcategories = QGroupBox("Add SubCategories")
        frm_add_categories = QFormLayout()
        frm_add_subcategories = QFormLayout()
        self.lne_category_name = QLineEdit()
        self.lne_subcategory_name = QLineEdit()
        self.cbx_category_type = QComboBox()
        self.cbx_categories = QComboBox()
        self.cbx_recurrent = QComboBox()
        self.cbx_recurrency = QComboBox()
        self.cbx_currencies = QComboBox()
        self.trw_categories = QTreeView()

        # setup the tree and model for categories
        # fetch categories and subcategories from model
        self.categories_list = self.presenter.get_category_list()
        self.subcategories_list = self.presenter.get_subcategory_list()
        # create the root/parent item list and add the children (subcategory) to them
        root_items = []
        for cat in self.categories_list:
            root_item = CategoryItem(f"{cat.category_type.value} - {cat.name}", cat.id)
            for subcat in self.subcategories_list:
                if subcat.category_id == cat.id:
                    root_item.addChild(CategoryItem(subcat.name, subcat.id, root_item))
            root_items.append(root_item)
        # send the items to the model and set it to the tree
        self.categories_model = CategoryModel(root_items)
        self.trw_categories.setModel(self.categories_model)
        # signals
        self.trw_categories.clicked.connect(self.handle_category_clicked)
        self.categories_model.categoryInserted.connect(lambda: self.on_model_row_inserted("category"))
        self.categories_model.subCategoryInserted.connect(lambda: self.on_model_row_inserted("subcategory"))

        # setup the user subcategories list and model
        # get the user categories from the model
        user_category_list = self.presenter.get_user_subcategory_list()
        # setup a list of user category items
        user_category_items: list = []
        for user_cat in user_category_list:
            user_category_items.append(
                UserCategoryItem(f"{user_cat.subcategory.category.name} - {user_cat.subcategory.name}", user_cat.id)
            )
        # send the user category list to the model and set it to the list table
        self.user_subcategory_list_model = CategoryListModel(user_category_items)
        self.lvw_user_categories.setModel(self.user_subcategory_list_model)

        self.starting_setup()

        # currencies setup
        self.cbx_currencies.currentTextChanged.connect(self.on_currency_change)

        # widgets with styles
        lbl_title_manage_categories = MainTitle("Manage expense categories")
        lbl_categories = SecondaryTitle("Category list")
        lbl_user_categories = SecondaryTitle("User categories")
        self.lbl_category_error_message = ErrorMessage("")
        self.lbl_subcategory_error_message = ErrorMessage("")
        current_currency = self.cbx_currencies.currentText()
        for currency in self.currency_list:
            if currency.getName() == current_currency:
                self.dsp_value = DoubleSpinBox(currency.getSymbol())

        # setup categories layout
        vbl_categories.addWidget(lbl_categories)
        vbl_categories.addWidget(self.trw_categories)
        vbl_categories.addLayout(hbl_add_categories)
        vbl_user_subcategories.addWidget(lbl_user_categories)
        vbl_user_subcategories.addWidget(self.lvw_user_categories)
        hbl_add_categories.addWidget(grb_add_categories, 1)
        hbl_add_categories.addWidget(grb_add_subcategories, 1)
        grb_add_categories.setLayout(vbl_add_categories)
        grb_add_subcategories.setLayout(vbl_add_subcategories)

        # setup categories form
        vbl_add_categories.addLayout(frm_add_categories)
        frm_add_categories.addRow("Category name", self.lne_category_name)
        frm_add_categories.addRow("Category type", self.cbx_category_type)
        vbl_add_categories.addWidget(self.lbl_category_error_message)
        vbl_add_categories.addWidget(btn_add_category)
        btn_add_category.clicked.connect(self.add_category)

        # setup subcategories form
        vbl_add_subcategories.addLayout(frm_add_subcategories)
        frm_add_subcategories.addRow("Parent category", self.cbx_categories)
        frm_add_subcategories.addRow("Sub-category name", self.lne_subcategory_name)
        self.cbx_recurrent.addItems(["Yes", "No"])
        frm_add_subcategories.addRow("Currency", self.cbx_currencies)
        frm_add_subcategories.addRow("Recurrency value", self.dsp_value)
        frm_add_subcategories.addRow("Recurrent", self.cbx_recurrent)
        self.cbx_recurrent.currentIndexChanged.connect(self.on_recurrent_change)
        frm_add_subcategories.addRow("Recurrency", self.cbx_recurrency)
        vbl_add_subcategories.addWidget(self.lbl_subcategory_error_message)
        vbl_add_subcategories.addWidget(btn_add_subcategory)
        btn_add_subcategory.clicked.connect(self.add_subcategory)

        # setup user categories buttons
        vbl_controls.addWidget(btn_select_users_categories)
        vbl_controls.addWidget(btn_remove_users_categories)
        btn_select_users_categories.clicked.connect(self.add_user_categories)
        btn_remove_users_categories.clicked.connect(self.remove_user_categories)

        # setup the vertical layouts inside the horizontal layout
        hbl_manage_categories.addLayout(vbl_categories, 6)
        hbl_manage_categories.addLayout(vbl_controls, 1)
        hbl_manage_categories.addLayout(vbl_user_subcategories, 2)

        # setup everything on the main layout
        vbl_main_layout.addWidget(lbl_title_manage_categories)
        vbl_main_layout.addLayout(hbl_manage_categories)

        # chose the horizontal layout as the main one
        self.setLayout(vbl_main_layout)

    def starting_setup(self):
        self.populate_currencies()
        # setup the categories for subcategory form
        self.populate_categories()
        # setup the category types for category form
        self.populate_category_type()
        # setup the recurrences for the subcategory form
        self.populate_recurrence()

    def add_category(self):
        data = self.get_category_data()
        new_category = self.presenter.create_category(data)
        if isinstance(new_category, str):
            self.set_error_message("category", new_category)
        else:
            new_category_item = CategoryItem(
                f"{new_category.category_type.value} - {new_category.name}", new_category.id
            )
            self.categories_model.addCategory(new_category_item)

    def add_subcategory(self):
        data = self.get_subcategory_data()
        category_name = data["category_name"]
        new_subcategory = self.presenter.create_subcategory(data)
        if isinstance(new_subcategory, str):
            self.set_error_message("subcategory", new_subcategory)
        else:
            root_items = self.categories_model.getCategories()
            for root_item in root_items:
                if root_item.data() == category_name:
                    self.categories_model.addSubcategory(
                        root_item, CategoryItem(new_subcategory.name, new_subcategory.id, root_item)
                    )

    def handle_category_clicked(self, index: QModelIndex):
        if not index.isValid():
            return

        # Check if the clicked item has children
        if self.categories_model.hasChildren(index):
            # Only collapse/expand if it's a category
            if self.trw_categories.isExpanded(index):
                self.trw_categories.collapse(index)
            else:
                self.trw_categories.collapseAll()
                self.trw_categories.expand(index)

                # Clear previous selections
                self.trw_categories.selectionModel().clearSelection()

                # Select the clicked item
                self.trw_categories.selectionModel().select(index, QItemSelectionModel.Select)

                # Select all children if it's a category
                childCount = self.categories_model.rowCount(index)
                for i in range(childCount):
                    childIndex = self.categories_model.index(i, 0, index)
                    self.trw_categories.selectionModel().select(childIndex, QItemSelectionModel.Select)

    def add_user_categories(self):
        selection_model = self.trw_categories.selectionModel()
        selected_indexes = selection_model.selectedIndexes()
        for index in selected_indexes:
            item = index.internalPointer()
            if len(item.children()) == 0:
                subcategory_id = item.id()
                new_user_subcategory = self.presenter.add_user_category(subcategory_id)
                if isinstance(new_user_subcategory, str):
                    # TODO need to add a place for error message here
                    print(new_user_subcategory)
                else:
                    self.user_subcategory_list_model.addUserCategory(
                        UserCategoryItem(
                            f"{new_user_subcategory.subcategory.category.name} - {new_user_subcategory.subcategory.name}",
                            new_user_subcategory.id,
                        )
                    )

    def remove_user_categories(self):
        selection_model = self.lvw_user_categories.selectionModel()
        selected_indexes = selection_model.selectedIndexes()
        for index in selected_indexes:
            item = index.internalPointer()
            # TODO handle errors from the db model
            self.presenter.remove_user_category(item.id())
            self.user_subcategory_list_model.removeUserCategory(index)

    def populate_categories(self):
        categories = self.categories_model.getCategories()
        self.cbx_categories.clear()
        self.cbx_categories.addItems(category.name for category in categories)

    def populate_recurrence(self):
        recurrence_list = self.presenter.get_recurrence()
        self.cbx_recurrency.clear()
        self.cbx_recurrency.addItems(recurrence for recurrence in recurrence_list if recurrence.name != "ONE")

    def populate_category_type(self):
        category_type_list = self.presenter.get_category_type()
        self.cbx_category_type.clear()
        self.cbx_category_type.addItems(category_type for category_type in category_type_list)

    def populate_currencies(self):
        all_currencies = self.presenter.get_currency()
        self.currency_list = [CurrencyItem(currency) for currency in all_currencies]
        self.cbx_currencies.clear()
        self.cbx_currencies.addItems([currency.getName() for currency in self.currency_list])

    def on_recurrent_change(self, _):
        if self.cbx_recurrent.currentText() == "No":
            self.cbx_recurrency.setDisabled(True)
        else:
            self.cbx_recurrency.setDisabled(False)

    def get_subcategory_data(self):
        return {
            "category_name": self.cbx_categories.currentText(),
            "name": self.lne_subcategory_name.text(),
            "recurrent": True if self.cbx_recurrent.currentText() == "Yes" else False,
            "recurrence": self.cbx_recurrency.currentText(),
            "recurrence_value": self.dsp_value.value() * 100,
            "currency": self.cbx_currencies.currentText(),
        }

    def get_category_data(self):
        return {"name": self.lne_category_name.text(), "category_type": self.cbx_category_type.currentText()}

    def on_currency_change(self):
        self.dsp_value.setPrefix(f"{self.currency_list[self.cbx_currencies.currentText()].value} ")

    def set_error_message(self, type: str, message: str) -> None:
        if type == "category":
            self.lbl_category_error_message.setText(message)
        if type == "subcategory":
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
        self.lbl_category_error_message.clear()
        self.lbl_subcategory_error_message.clear()
        # Stop the timer after clearing the messages
        if self.clear_timer:
            self.clear_timer.stop()

    def on_model_row_inserted(self, type: str):
        if type == "category":
            self.populate_categories()
            self.clear_category_data()
        if type == "subcategory":
            self.clear_subcategory_data()

    def clear_category_data(self):
        self.lne_category_name.clear()
        self.cbx_category_type.setCurrentIndex(0)

    def clear_subcategory_data(self):
        self.cbx_categories.setCurrentIndex(0)
        self.lne_subcategory_name.clear()
        self.cbx_recurrent.setCurrentIndex(0)
        self.cbx_recurrency.setCurrentIndex(0)
        self.dsp_value.setValue(0.00)
        self.cbx_currencies.setCurrentIndex(0)

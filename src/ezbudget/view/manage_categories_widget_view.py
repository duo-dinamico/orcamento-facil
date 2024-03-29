from PySide6.QtCore import QAbstractListModel, Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QListView,
    QPushButton,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)


class CategoryListModel(QAbstractListModel):
    def __init__(self, categories):
        super().__init__()
        self.categories = categories
        self.headers = ["User Categories"]

    def rowCount(self, _):
        return len(self.categories)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            user_subcategory = self.categories[index.row()]
            return user_subcategory


class Categories(QWidget):
    def __init__(self, presenter):
        super().__init__()
        self.presenter = presenter

        # instances of necessary widgets
        hbl_manage_categories = QHBoxLayout()
        hbl_add_categories = QHBoxLayout()
        vbl_controls = QVBoxLayout()
        vbl_categories = QVBoxLayout()
        vbl_add_categories = QVBoxLayout()
        vbl_add_subcategories = QVBoxLayout()
        btn_select_users_categories = QPushButton(">>")
        btn_remove_users_categories = QPushButton("<<")
        btn_add_category = QPushButton("Add category")
        btn_add_subcategory = QPushButton("Add sub-category")
        self.lvw_user_categories = QListView(self)
        self.trw_categories = QTreeWidget(self)
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
        self.dsp_value = QDoubleSpinBox()

        # setup the list / tree
        self.trw_categories.setHeaderLabels(["Categories"])
        self.trw_categories.itemClicked.connect(self.handle_category_clicked)

        # setup categories in treeview
        self.set_categories_and_subcategories()

        # setup categories layout
        vbl_categories.addWidget(self.trw_categories)
        vbl_categories.addLayout(hbl_add_categories)
        hbl_add_categories.addWidget(grb_add_categories, 1)
        hbl_add_categories.addWidget(grb_add_subcategories, 1)
        grb_add_categories.setLayout(vbl_add_categories)
        grb_add_subcategories.setLayout(vbl_add_subcategories)

        # setup categories form
        vbl_add_categories.addLayout(frm_add_categories)
        frm_add_categories.addRow("Category name", self.lne_category_name)
        frm_add_categories.addRow("Category type", self.cbx_category_type)
        vbl_add_categories.addWidget(btn_add_category)
        btn_add_category.clicked.connect(lambda: self.presenter.create_category(self.get_category_data()))

        # setup subcategories form
        vbl_add_subcategories.addLayout(frm_add_subcategories)
        frm_add_subcategories.addRow("Parent category", self.cbx_categories)
        frm_add_subcategories.addRow("Sub-category name", self.lne_subcategory_name)
        self.cbx_recurrent.addItems(["Yes", "No"])
        frm_add_subcategories.addRow("Recurrent", self.cbx_recurrent)
        self.cbx_recurrent.currentIndexChanged.connect(self.on_recurrent_change)
        frm_add_subcategories.addRow("Recurrency", self.cbx_recurrency)
        frm_add_subcategories.addRow("Recurrency value", self.dsp_value)
        frm_add_subcategories.addRow("Currency", self.cbx_currencies)
        frm_add_subcategories.addRow(btn_add_subcategory)
        btn_add_subcategory.clicked.connect(lambda: self.presenter.create_subcategory(self.get_subcategory_data()))

        # configure value entry
        self.populate_currencies()
        self.dsp_value.setMaximum(999999.99)
        self.dsp_value.setMinimum(-999999.99)
        self.dsp_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.dsp_value.setPrefix(f"{self.currency_list[self.cbx_currencies.currentText()].value} ")
        self.cbx_currencies.currentTextChanged.connect(self.on_currency_change)

        # setup user categories buttons
        vbl_controls.addWidget(btn_select_users_categories)
        vbl_controls.addWidget(btn_remove_users_categories)
        btn_select_users_categories.clicked.connect(self.add_user_categories)
        btn_remove_users_categories.clicked.connect(self.remove_user_categories)

        # setup the vertical layouts inside the horizontal layout
        hbl_manage_categories.addLayout(vbl_categories, 5)
        hbl_manage_categories.addLayout(vbl_controls, 1)
        hbl_manage_categories.addWidget(self.lvw_user_categories, 3)

        # chose the horizontal layout as the main one
        self.set_categories_model()
        self.populate_recurrence()
        self.setLayout(hbl_manage_categories)

    def set_categories_and_subcategories(self):
        self.categories = self.presenter.get_category_list()
        self.subcategories = self.presenter.get_subcategory_list()

        self.populate_categories(self.categories)
        self.populate_category_type()

        self.trw_categories.clear()

        for category in self.categories:
            tree_category = QTreeWidgetItem(self.trw_categories, [f"{category.category_type.value} - {category.name}"])
            tree_category.setData(0, Qt.UserRole, f"CAT-{category.id}")
            for subcategory in self.subcategories:
                if subcategory.category_id == category.id:
                    tree_subcategory = QTreeWidgetItem(tree_category, [subcategory.name])
                    tree_subcategory.setData(0, Qt.UserRole, f"SUB-{subcategory.id}")

    def handle_category_clicked(self, item, _):
        if item.childCount() > 0:
            item.setExpanded(True)
            for index in range(item.childCount()):
                subcategory = item.child(index)
                subcategory.setSelected(True)

    def set_categories_model(self):
        user_subcategory_list = self.presenter.get_user_subcategory_list()
        category_with_subcategory: list = [user_subcategory[0] for user_subcategory in user_subcategory_list]
        self.user_subcategory_list_model = CategoryListModel(category_with_subcategory)
        self.lvw_user_categories.setModel(self.user_subcategory_list_model)

    def add_user_categories(self):
        selection_model = self.trw_categories.selectionModel()
        selected_indexes = selection_model.selectedIndexes()
        for index in selected_indexes:
            index_data = index.data(Qt.UserRole)
            if index_data.startswith("SUB"):
                split_index_data = index_data.split("-")
                self.presenter.add_user_category(split_index_data[1])
        self.set_categories_model()

    def remove_user_categories(self):
        selection_model = self.lvw_user_categories.selectionModel()
        selected_indexes = selection_model.selectedIndexes()
        for index in selected_indexes:
            split_index_data = index.data().split(" - ")
            category_id = self.presenter.get_category_id_by_name(split_index_data[0])
            subcategory_id = self.presenter.get_subcategory_id_by_name_and_category(split_index_data[1], category_id)
            self.presenter.remove_user_category(subcategory_id)
        self.set_categories_model()

    def populate_categories(self, categories):
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
        self.currency_list = self.presenter.get_currency()
        self.cbx_currencies.clear()
        self.cbx_currencies.addItems([currency.name for currency in self.currency_list])

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

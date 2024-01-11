from PySide6.QtCore import QAbstractListModel, Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
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
        vbl_controls = QVBoxLayout()
        btn_select_users_categories = QPushButton(">>")
        btn_remove_users_categories = QPushButton("<<")
        self.lvw_user_categories = QListView(self)
        self.trw_categories = QTreeWidget(self)

        # setup the list / tree
        self.trw_categories.setHeaderLabels(["Categories"])
        self.trw_categories.itemClicked.connect(self.handle_category_clicked)

        # setup categories in treeview
        self.set_categories_and_subcategories()

        # setup buttons
        vbl_controls.addWidget(btn_select_users_categories)
        vbl_controls.addWidget(btn_remove_users_categories)
        btn_select_users_categories.clicked.connect(self.add_user_categories)
        btn_remove_users_categories.clicked.connect(self.remove_user_categories)

        # setup the vertical layouts inside the horizontal layout
        hbl_manage_categories.addWidget(self.trw_categories, 5)
        hbl_manage_categories.addLayout(vbl_controls, 1)
        hbl_manage_categories.addWidget(self.lvw_user_categories, 5)

        # chose the horizontal layout as the main one
        self.set_categories_model()
        self.setLayout(hbl_manage_categories)

    def set_categories_and_subcategories(self):
        self.categories = self.presenter.get_category_list()
        self.subcategories = self.presenter.get_subcategory_list()

        for category in self.categories:
            tree_category = QTreeWidgetItem(self.trw_categories, [category.name])
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
        self.user_subcategory_list = self.presenter.get_user_subcategory_list()
        self.user_subcategory_list_model = CategoryListModel(self.user_subcategory_list)
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

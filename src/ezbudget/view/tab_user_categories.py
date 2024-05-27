from PySide6.QtWidgets import (
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QListView,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ezbudget.view.models import AbstractListModel, UserCategoryItem
from ezbudget.view.styles import MainTitle


class UserCategories(QWidget):
    def __init__(self, parent, presenter):
        super().__init__()
        self._parent = parent
        self.presenter = presenter

        # instances of necessary widgets
        hbl_select_user_categories = QHBoxLayout()
        vbl_main_layout = QVBoxLayout()
        vbl_controls = QVBoxLayout()
        vbl_categories = QVBoxLayout()
        vbl_user_subcategories = QVBoxLayout()
        btn_select_users_categories = QPushButton("    >>    ")
        btn_remove_users_categories = QPushButton("    <<    ")
        self.lvw_subcategories = QListView(self)
        self.lvw_user_categories = QListView(self)
        self.lne_category_name = QLineEdit()
        self.cbx_category_type = QComboBox()
        self.cbx_categories = QComboBox()
        grb_categories = QGroupBox("Category list")
        grb_user_categories = QGroupBox("User categories")

        self.subcategories_model = AbstractListModel()
        self.user_subcategory_list_model = AbstractListModel()
        self.lvw_subcategories.setModel(self.subcategories_model)
        self.lvw_subcategories.setSelectionMode(QListView.MultiSelection)
        self.lvw_user_categories.setModel(self.user_subcategory_list_model)

        # widgets with styles
        lbl_title_manage_categories = MainTitle("User Categories")

        # setup categories layout
        vbl_categories.addWidget(self.lvw_subcategories)
        grb_categories.setLayout(vbl_categories)
        vbl_user_subcategories.addWidget(self.lvw_user_categories)
        grb_user_categories.setLayout(vbl_user_subcategories)

        # setup user categories buttons
        vbl_controls.addWidget(btn_select_users_categories)
        vbl_controls.addWidget(btn_remove_users_categories)
        btn_select_users_categories.clicked.connect(self.add_user_categories)
        btn_remove_users_categories.clicked.connect(self.remove_user_categories)

        # setup the vertical layouts inside the horizontal layout
        hbl_select_user_categories.addWidget(grb_categories)
        hbl_select_user_categories.addLayout(vbl_controls)
        hbl_select_user_categories.addWidget(grb_user_categories)

        # setup everything on the main layout
        vbl_main_layout.addWidget(lbl_title_manage_categories)
        vbl_main_layout.addLayout(hbl_select_user_categories)

        # signals
        self._parent.categories.subcategories_model.rowsInserted.connect(self.refresh_subcategory_model_data)
        self._parent.categories.subcategories_model.rowsRemoved.connect(self.refresh_subcategory_model_data)
        self._parent.categories.subcategories_model.modelReset.connect(self.refresh_subcategory_model_data)
        self._parent.categories.subcategories_model.modelReset.connect(self.refresh_user_category_model_data)
        btn_select_users_categories.clicked.connect(self.add_user_categories)
        btn_remove_users_categories.clicked.connect(self.remove_user_categories)

        # initial setup
        self.starting_setup()

        # chose the horizontal layout as the main one
        self.setLayout(vbl_main_layout)

    def fetch_data(self):
        self.subcategories_list = self.presenter.get_subcategory_list()
        self.user_category_list = self.presenter.get_user_subcategory_list()

    def starting_setup(self):
        self.fetch_data()
        self.refresh_subcategory_model_data()
        self.refresh_user_category_model_data()

    def refresh_subcategory_model_data(self):
        self.fetch_data()
        present_in_user_categories = list(
            set([s.id for s in self.subcategories_list]).intersection(
                set([u.subcategory.id for u in self.user_category_list])
            )
        )
        current_subcategories: list = []
        for subcategory in self.subcategories_list:
            if subcategory.id not in present_in_user_categories:
                subcategory_item = UserCategoryItem(subcategory)
                current_subcategories.append(subcategory_item)
        self.subcategories_model.setObjects(current_subcategories)

    def refresh_user_category_model_data(self):
        self.fetch_data()
        current_user_categories: list = []
        for user_category in self.user_category_list:
            user_category_item = UserCategoryItem(user_category.subcategory)
            current_user_categories.append(user_category_item)
        self.user_subcategory_list_model.setObjects(current_user_categories)

    def add_user_categories(self):
        selection_model = self.lvw_subcategories.selectionModel()
        selected_indexes = selection_model.selectedIndexes()
        for index in selected_indexes:
            item: UserCategoryItem = index.internalPointer()
            subcategory_id = item.getId()
            new_user_subcategory = self.presenter.add_user_category(subcategory_id)
            if isinstance(new_user_subcategory, str):
                # TODO need to add a place for error message here
                print(f"add new user category - {new_user_subcategory}")
            else:
                new_user_subcategory_item = UserCategoryItem(new_user_subcategory.subcategory)
                self.user_subcategory_list_model.addListItem(new_user_subcategory_item)
        self.fetch_data()
        self.refresh_subcategory_model_data()
        self.refresh_user_category_model_data()

    def remove_user_categories(self):
        selection_model = self.lvw_user_categories.selectionModel()
        selected_indexes = selection_model.selectedIndexes()
        for index in selected_indexes:
            item: UserCategoryItem = index.internalPointer()
            response = self.presenter.remove_user_category(item.getId())
            if isinstance(response, str):
                # TODO need to add a place for error message here
                print(response)
            else:
                self.user_subcategory_list_model.removeListItem(index)
        self.fetch_data()
        self.refresh_subcategory_model_data()
        self.refresh_user_category_model_data()

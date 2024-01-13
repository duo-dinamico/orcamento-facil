from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from ezbudget.model import Category, CategoryTypeEnum


class ModelCategory:
    def __init__(self, parent_model):
        self.parent = parent_model

    def create_category(self, name: str, category_type: CategoryTypeEnum) -> Category | None:
        """Create a new category in the database, and return the category.

        Args:
            name: name of the new category.
            category_type: type of category, either a Want a Need or a Saving

        Returns:
            category: if a new category was created
            None: if the category failed to be created.
        """
        try:
            category = Category(name=name, category_type=category_type)
            self.parent.session.add(category)
            self.parent.session.commit()
            self.parent.session.refresh(category)

            return category
        except IntegrityError:
            return "Category already exists"

    def read_category_by_name(self, name: str) -> Category | None:
        """Return a category id that has the given name.

        Args:
            name: the category name.

        Returns:
            category: if the category exist.
            None: if the category don't exist.
        """
        try:
            return self.parent.read_first_basequery(select(Category).where(Category.name == name))
        except NoResultFound:
            return None

    def read_category_by_id(self, id: int) -> Category | None:
        """Return a category object that has the given category id.

        Args:
            id: the category id.

        Returns:
            category: category object, if the category exist.
            None: if the category does not exist.
        """
        try:
            return self.parent.read_first_basequery(select(Category).where(Category.id == id))
        except NoResultFound:
            return None

    def read_categories(self) -> list:
        """Return a list of all categories.

        Returns:
            category_list: list of all categories.
        """
        return self.parent.read_all_basequery(select(Category))

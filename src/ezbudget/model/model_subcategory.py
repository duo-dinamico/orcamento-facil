from sqlalchemy import and_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from ezbudget.model import RecurrenceEnum, SubCategory


class ModelSubCategory:
    def __init__(self, parent_model):
        self.parent = parent_model

    def create_subcategory(
        self,
        category_id: int,
        name: str,
        recurrent: bool = False,
        recurrence: RecurrenceEnum = "ONE",
        include: bool = True,
    ) -> SubCategory | None:
        """Create a new subcategory in the database, and return the subcategory.

        Args:
            name: name of the new subcategory.

        Returns:
            subcategory: if a new subcategory was created
            None: if the subcategory failed to be created.
        """
        try:
            new_subcategory = SubCategory(
                category_id=category_id,
                name=name,
                recurrent=recurrent,
                recurrence=recurrence,
                include=include,
            )

            self.parent.session.add(new_subcategory)
            self.parent.session.commit()
            self.parent.session.refresh(new_subcategory)
            return new_subcategory
        except IntegrityError as e:
            if "foreign key constraint" in str(e.orig).lower():
                return "Category ID does not exist"
            else:
                return "An unknown IntegrityError occurred"
        except LookupError as lookup_error:
            return f"A LookupError occurred: {lookup_error}"

    def read_subcategory_by_name(self, name: str, category_id: int) -> SubCategory | None:
        """Return a subcategory id that has the given subcategory name.

        Args:
            name: the subcategory name.
            category_id: category id to filter as names are not unique

        Returns:
            subcategory: if the subcategory exist.
            None: if the subcategory don't exist.
        """
        try:
            return self.parent.read_first_basequery(
                select(SubCategory).where(and_(SubCategory.name == name, SubCategory.category_id == category_id))
            )
        except NoResultFound:
            return None

    def read_subcategories_by_category_id(self, category_id: int) -> list:
        """Return a list of all subcategories from a given category id.

        Args:
            category_id: category id from where we get the subcategories list

        Returns:
            subcategory_list: list of all subcategories for a given category id.
        """
        try:
            return self.parent.read_all_basequery(select(SubCategory).where(SubCategory.category_id == category_id))
        except NoResultFound:
            return []

    def read_subcategories(self) -> list:
        """Return a list of all subcategories.

        Returns:
            subcategory_list: list of all subcategories.
        """
        return self.parent.read_all_basequery(select(SubCategory))

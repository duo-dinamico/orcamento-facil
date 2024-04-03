from sqlalchemy import and_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from ezbudget.model import UserSubCategory


class ModelUserSubCategory:
    def __init__(self, parent_model):
        self.parent = parent_model

    def create_user_subcategory(self, user_id: int, subcategory_id: int) -> UserSubCategory | None:
        """Create a new user and subcategory relationship.

        Args:
            user_id: the id of the user.
            subcategory_id: the id of the subcategory.

        Returns:
            UserSubCategory: if the relationship was created
            None: if it failed to create.
        """
        try:
            new_user_subcategory = UserSubCategory(
                user_id=user_id,
                subcategory_id=subcategory_id,
            )

            self.parent.session.add(new_user_subcategory)
            self.parent.session.commit()
            self.parent.session.refresh(new_user_subcategory)
            return new_user_subcategory
        except IntegrityError as e:
            self.parent.session.rollback()
            if "foreign key constraint" in str(e.orig).lower():
                return "Either User ID or SubCategory ID does not exist"
            # TODO create unique constraint of the columns and test it
            elif "unique constraint" in str(e.orig).lower():
                return "User ID and SubCategory ID combination must be unique"
            else:
                return "An unknown IntegrityError occurred"

    def read_user_subcategories_multiple_args(self, **kwargs) -> UserSubCategory | None:
        """Return a user subcategory from given key-value pairs.

        Args:
            **kwargs: key-value pairs to filter on

        Returns:
            UserSubCategory: a user subcategory for given key-value pairs.
            None: if the user subcategory does not exist.
        """
        try:
            filters = [getattr(UserSubCategory, key) == value for key, value in kwargs.items()]
            query = select(UserSubCategory).where(and_(*filters))
            return self.parent.read_first_basequery(query)
        except NoResultFound:
            return None
        except AttributeError as e:
            return f"AttributeError: {e.args[0]}"

    def read_user_subcategories_single_arg(self, key: str, value: str | int) -> UserSubCategory | None:
        """Return a user subcategory from a given key-value pair.

        Args:
            key: the name of the column to filter on
            value: the value to filter on

        Returns:
            UserSubCategory: a user subcategory for given key-value pairs.
            None: if the user subcategory does not exist.
        """
        try:
            query = select(UserSubCategory).where(getattr(UserSubCategory, key) == value)
            return self.parent.read_first_basequery(query)
        except NoResultFound:
            return None
        except AttributeError as e:
            return f"AttributeError: {e.args[0]}"

    def read_user_subcategories_by_user(self, user_id: int) -> list | None:
        """Return a list of user subcategory from a given user.

        Args:
            user_id: the user to filter the list

        Returns:
            list: a list of user subcategories for given user id.
            None: if the user does not have any user subcategories selected.
        """
        return self.parent.read_all_basequery(select(UserSubCategory).where(UserSubCategory.user_id == user_id))

    def delete_user_subcategory(self, id: int) -> int:
        """Removes a user subcategory relationship for a given id.

        Args:
            id: the id of the subcategory.

        Returns:
            int: the number of deleted rows
        """
        # TODO Delete and update are under consideration due to the risk of permanent changes
        deleted_row = self.parent.session.query(UserSubCategory).where(UserSubCategory.id == id).delete()
        self.parent.session.commit()
        return deleted_row

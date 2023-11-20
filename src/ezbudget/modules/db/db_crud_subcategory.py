from sqlalchemy import select

from ezbudget.model import Model, RecurrenceEnum, SubCategory

from .db_crud_category import read_category_by_id

db = Model()


def read_subcategory_by_name(db: db.session, name: str) -> int:
    """Return a subcategory id that has the given subcategory name.

    Args:
        db: database session.
        name: the subcategory name.

    Returns:
        subcategory_id: if the subcategory exist.
        None: if the subcategory don't exist.
    """
    subcategory = db.scalars(select(SubCategory).where(SubCategory.name == name)).first()
    if not subcategory:
        return None
    return subcategory.id


def read_subcategory_list_by_category_id(db: db.session, category_id: int) -> list:
    """Return a list of all subcategories from a given category id.

    Args:
        db: database session.
        category_id: category id from where we get the subcategories list

    Returns:
        subcategory_list: list of all subcategories for a given category id, if there is at least one subcategory.
        None: if there is no subcategory, or category_id.
    """

    # Check if the category_id exists
    category = read_category_by_id(db, category_id=category_id)
    if not category:
        return None

    subcategory_list = db.scalars(select(SubCategory).where(SubCategory.category_id == category_id)).all()
    if len(subcategory_list) == 0:
        return None
    return subcategory_list


def create_subcategory(
    db: db.session,
    category_id: int,
    name: str,
    recurrent: bool = False,
    recurrence: RecurrenceEnum = "ONE",
    include: bool = True,
) -> int:
    """Create a new subcategory in the database, and return the subcategory id.

    Args:
        db: database session.
        name: name of the new subcategory.

    Returns:
        subcategory_id: if a new subcategory was created
        None: if the subcategory failed to be created.
    """
    # Check if name already exist
    subcategory = read_subcategory_by_name(db, name=name)
    if subcategory:
        return None

    # Check if category_id exist
    category = read_category_by_id(db, category_id=category_id)
    if not category:
        return None

    # Check if boolean
    if not isinstance(recurrent, bool) or not isinstance(include, bool):
        return None

    # Check if recurrence is valid
    if recurrence not in RecurrenceEnum.__members__:
        return None

    # Add subcategory to the database
    db_subcategory = SubCategory(
        category_id=category_id,
        name=name,
        recurrent=recurrent,
        recurrence=recurrence,
        include=include,
    )
    db.add(db_subcategory)
    db.commit()
    db.refresh(db_subcategory)
    return db_subcategory.id

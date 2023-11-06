from sqlalchemy import select
from datetime import datetime

from modules.utils.logging import logger

from modules.db_database import SessionLocal
from modules.db_models import Category


def read_category_by_name(db: SessionLocal, name: str) -> int:
    """Return a category id that has the given name.

    Args:
        db: database session.
        name: the category name.

    Returns:
        category_id: if the category exist.
        None: if the category don't exist.
    """
    category = db.scalars(select(Category).where(Category.name == name)).first()
    logger.info(f"read_category_by_name: {category}")
    if not category:
        return None
    return category.id


def create_category(db: SessionLocal, name: str) -> int:
    """Create a new category in the database, and return the category id.

    Args:
        db: database session.
        name: name of the new category.

    Returns:
        category_id: if a new category was created
        None: if the category failed to be created.
    """
    # Check if name already exist
    category = read_category_by_name(db, name=name)
    if category:
        logger.info(f"category already exist with ID: {category}.")
        return None

    # Add category to the database
    db_category = Category(name=name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    logger.info(f"category created: {db_category}.")
    return db_category.id

from sqlalchemy import select

from ..utils.logging import logger
from .db_crud_account import read_account_by_id
from .db_database import SessionLocal
from .db_models import Income, MonthEnum, RecurrencyEnum


def read_income_by_name(db: SessionLocal, name: str) -> int:
    """Return an income id that has the given name.

    Args:
        db: database session.
        income_name: the income name.

    Returns:
        income_id: if the income exist.
        None: if the income don't exist.
    """
    income = db.scalars(select(Income).where(Income.name == name)).first()
    logger.info(f"read income by name: {income} --- {name}")
    if not income:
        return None
    return income.id


def create_income(
    db: SessionLocal,
    account_id: int,
    name: str,
    expected_income_value: int = 0,
    real_income_value: int = 0,
    income_day: str = "1",
    income_month: MonthEnum = MonthEnum.JANUARY,
    recurrency: RecurrencyEnum = RecurrencyEnum.ONE,
) -> int:
    """Create a new income, for a given account and return the new income id.

    Args:
        db: database session.
        account_id: the account id for the income.
        name: name of the income.
        expected_income_value: expected value of the income in cents, it's zero by default.
        real_income_value: real value of the income in cents, it's zero by default.
        income_day: the day of the month of the first income, it's 1 by default.
        income_month: the month of the income, from an enum.
        recurrency: recurrency of the income, from an enum, it's ONE by default.

    Returns:
        account_id: if a new account was created.
        None: if the user_id is not valid or if the account name already exists.
    """

    # Check if the account_id is valid
    account = read_account_by_id(db, account_id=account_id)
    if not account:
        logger.info(f"Account don't exist: {account_id}.")
        return None

    # Check if the income name already exist
    income = read_income_by_name(db, name=name)
    if income:
        logger.info(f"Income name already exist: {name}.")
        return None

    logger.info(f"create_income: {account_id} {name}")

    # Add income to the database
    db_income = Income(
        account_id=account_id,
        name=name,
        expected_income_value=expected_income_value,
        real_income_value=real_income_value,
        income_day=income_day,
        income_month=income_month,
        recurrency=recurrency,
    )
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income.id


def delete_income(db: SessionLocal, income_id: int) -> bool:
    """Delete an income in the database.

    Args:
        db: database session.
        income_id: id of the income to delete.

    Returns:
        True: if deleted.
        False: if not deleted.
    """

    # Check if income exist
    income = db.scalars(select(Income).where(Income.id == income_id)).first()
    if not income:
        logger.info(f"income_id don't exist: {income}")
        return False

    # Delete the income
    db.delete(income)
    db.commit()
    logger.info(f"deleted income: {income_id}")
    return True

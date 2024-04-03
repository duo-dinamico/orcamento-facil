from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


# Define an enum type for account types
class AccountTypeEnum(str, Enum):
    BANK = "Bank"
    CARD = "Credit Card"
    CASH = "Cash"


# Define an enum type for recurrence
class RecurrenceEnum(str, Enum):
    ONE = "One time only"
    DAY = "Daily"
    WEEK = "Weekly"
    MONTH = "Monthly"
    YEAR = "Yearly"


class CurrencyEnum(str, Enum):
    EUR = "€"
    GBP = "£"
    USD = "$"
    JPY = "¥"


class CategoryTypeEnum(str, Enum):
    NEED = "Need"
    WANT = "Want"
    SAVINGS = "Savings"
    DEBT = "Debt"


class TransactionTypeEnum(str, Enum):
    Income = "+"
    Expense = "-"
    Transfer = "<- ->"


class User(Base):
    __tablename__ = "users"

    # mandatory
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)


class Account(Base):
    __tablename__ = "accounts"

    # mandatory
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", name="user"), nullable=False)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    account_type: Mapped[AccountTypeEnum] = mapped_column(nullable=False)
    currency: Mapped[CurrencyEnum] = mapped_column(nullable=False)
    balance: Mapped[int] = mapped_column(default=0)  # In cents

    # optional
    credit_limit: Mapped[Optional[int]]  # In cents
    payment_day: Mapped[Optional[str]]  # Saved as a string, need conversion
    interest_rate: Mapped[Optional[float]]
    credit_method: Mapped[Optional[str]]

    # relatioships
    user: Mapped["User"] = relationship("User")


class Income(Base):
    __tablename__ = "incomes"

    # mandatory
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", name="user"), nullable=False)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id", name="account"), nullable=False)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    recurrence_value: Mapped[int] = mapped_column(default=0)  # In cents
    currency: Mapped[CurrencyEnum] = mapped_column(nullable=False)
    recurrent: Mapped[bool] = mapped_column(default=False)

    # optional
    income_date: Mapped[Optional[datetime]]
    recurrence: Mapped[Optional[RecurrenceEnum]]

    # Relationships
    user: Mapped["User"] = relationship("User")
    account: Mapped["Account"] = relationship("Account")


class Transaction(Base):
    __tablename__ = "transactions"

    # mandatory
    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False)
    subcategory_id: Mapped[int] = mapped_column(ForeignKey("subcategories.id", name="subcategory"), nullable=False)
    transaction_type: Mapped[TransactionTypeEnum] = mapped_column(nullable=False)
    value: Mapped[int] = mapped_column(default=0)  # In cents
    currency: Mapped[CurrencyEnum] = mapped_column(nullable=False)
    date: Mapped[datetime]

    # optional
    description: Mapped[Optional[str]]
    target_account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=True)

    # relatioships
    account: Mapped["Account"] = relationship("Account", foreign_keys=[account_id])
    target_account: Mapped["Account"] = relationship("Account", foreign_keys=[target_account_id])
    subcategory: Mapped["SubCategory"] = relationship("SubCategory")


class SubCategory(Base):
    __tablename__ = "subcategories"

    # mandatory
    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", name="category"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    recurrent: Mapped[bool] = mapped_column(default=False)

    # optional
    recurrence: Mapped[Optional[RecurrenceEnum]]
    currency: Mapped[Optional[CurrencyEnum]]
    recurrence_value: Mapped[Optional[int]]

    # relatioships
    category: Mapped["Category"] = relationship("Category")


class Category(Base):
    __tablename__ = "categories"

    # mandatory
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    category_type: Mapped[CategoryTypeEnum] = mapped_column(nullable=False)


class UserSubCategory(Base):
    __tablename__ = "usersubcategories"

    # mandatory
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", name="user"), nullable=False)
    subcategory_id: Mapped[int] = mapped_column(ForeignKey("subcategories.id", name="subcategory"), nullable=False)

    # relationships
    subcategory: Mapped["SubCategory"] = relationship("SubCategory")
    __table_args__ = (UniqueConstraint("user_id", "subcategory_id", name="uniq_user_subcategory"),)

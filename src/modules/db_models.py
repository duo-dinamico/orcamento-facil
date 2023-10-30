from enum import Enum
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Optional


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    accounts: Mapped["Account"] = relationship("Account", backref="accounts", uselist=False)

    def __str__(self) -> str:
        return f"ID: {self.id}, Name: {self.username}."


# Define an enum type for account types
class AccountTypeEnum(str, Enum):
    BANK = "Bank"
    CARD = "Credit Card"
    CASH = "Cash"


# Define an enum type for recurrency
class RecurrencyEnum(str, Enum):
    ONE = "One time only"
    DAY = "Daily"
    MONTH = "Monthly"
    YEAR = "Yearly"


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", name="user"))
    name: Mapped[str] = mapped_column(unique=True)
    account_type: Mapped[AccountTypeEnum]
    currency: Mapped[str] = mapped_column(default="EUR")
    initial_balance: Mapped[int] = mapped_column(default=0)  # In cents
    balance: Mapped[int] = mapped_column(default=0)  # In cents
    credit_limit: Mapped[Optional[int]]  # In cents
    payment_day: Mapped[Optional[str]]  # Saved as a string, need conversion
    interest_rate: Mapped[Optional[float]]
    credit_method: Mapped[Optional[str]]


class Income(Base):
    __tablename__ = "incomes"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id", name="account"))
    name: Mapped[str] = mapped_column(unique=True)
    expected_income_value: Mapped[int] = mapped_column(default=0)  # In cents
    real_income_value: Mapped[int] = mapped_column(default=0)  # In cents
    income_day: Mapped[Optional[str]]  # Saved as a string, need conversion
    recurrency: Mapped[RecurrencyEnum]


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id", name="account"))
    subcategory_id: Mapped[int] = mapped_column(ForeignKey("subcategories.id", name="subcategory"))
    date: Mapped[datetime]
    value: Mapped[int] = mapped_column(default=0)  # In cents
    description: Mapped[Optional[str]]


class SubCategories(Base):
    __tablename__ = "subcategories"

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", name="category"))
    name: Mapped[str] = mapped_column(unique=True)
    recurrent: Mapped[bool] = mapped_column(default=False)
    recurrency: Mapped[RecurrencyEnum]
    include: Mapped[bool] = mapped_column(default=True)


class Categories(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

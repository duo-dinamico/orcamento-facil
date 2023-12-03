from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    accounts: Mapped["Account"] = relationship("Account", backref="accounts", uselist=False)

    def __str__(self) -> str:
        return f"ID: {self.id}, Name: {self.username}"


# Define an enum type for account types
class AccountTypeEnum(str, Enum):
    BANK = "Bank"
    CARD = "Credit Card"
    CASH = "Cash"


# Define an enum type for recurrence
class RecurrenceEnum(str, Enum):
    ONE = "One time only"
    DAY = "Daily"
    MONTH = "Monthly"
    YEAR = "Yearly"


# Define an enum type for months
class MonthEnum(int, Enum):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12


class CurrencyEnum(str, Enum):
    EUR = "€"
    GBP = "£"
    USD = "$"


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", name="user"))
    name: Mapped[str] = mapped_column(unique=True)
    account_type: Mapped[AccountTypeEnum] = mapped_column(default="BANK")
    currency: Mapped[CurrencyEnum] = mapped_column(default="EUR")
    balance: Mapped[int] = mapped_column(default=0)  # In cents
    credit_limit: Mapped[Optional[int]]  # In cents
    payment_day: Mapped[Optional[str]]  # Saved as a string, need conversion
    interest_rate: Mapped[Optional[float]]
    credit_method: Mapped[Optional[str]]

    # Relatioships
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="account")

    def __str__(self) -> str:
        return f"ID: {self.id}, Name: {self.name}"


class Income(Base):
    __tablename__ = "incomes"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", name="user"))
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id", name="account"))
    name: Mapped[str] = mapped_column(unique=True)
    expected_income_value: Mapped[int] = mapped_column(default=0)  # In cents
    real_income_value: Mapped[int] = mapped_column(default=0)  # In cents
    income_day: Mapped[Optional[str]] = mapped_column(default="1")  # Saved as a string, need conversion
    income_month: Mapped[Optional[MonthEnum]] = mapped_column(default=MonthEnum.JANUARY)
    recurrence: Mapped[Optional[RecurrenceEnum]] = mapped_column(default=RecurrenceEnum.ONE)

    def __str__(self) -> str:
        return f"ID: {self.id}, Name: {self.name}, Account ID: {self.account_id}"


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id", name="account"))
    subcategory_id: Mapped[int] = mapped_column(ForeignKey("subcategories.id", name="subcategory"))
    date: Mapped[datetime]
    value: Mapped[int] = mapped_column(default=0)  # In cents
    description: Mapped[Optional[str]]

    # Relatioships
    account: Mapped["Account"] = relationship(back_populates="transactions")


class SubCategory(Base):
    __tablename__ = "subcategories"

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", name="category"))
    name: Mapped[str]
    recurrent: Mapped[bool] = mapped_column(default=False)
    recurrence: Mapped[Optional[RecurrenceEnum]]
    # TODO we can remove this include since we have the connection table
    include: Mapped[bool] = mapped_column(default=True)


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)


class UserSubCategory(Base):
    __tablename__ = "usersubcategories"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", name="user"))
    subcategory_id: Mapped[int] = mapped_column(ForeignKey("subcategories.id", name="subcategory"))
    subcategory: Mapped["SubCategory"] = relationship("SubCategory")
    __table_args__ = (UniqueConstraint("user_id", "subcategory_id", name="uniq_user_subcategory"),)

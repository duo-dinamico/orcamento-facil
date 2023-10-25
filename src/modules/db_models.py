from enum import Enum

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


# Define an enum type for account types
class AccountTypeEnum(str, Enum):
    BANK = "Bank"
    CARD = "Credit Card"
    CASH = "Cash"


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
    payment_day: Mapped[Optional[str]]
    interest_rate: Mapped[Optional[float]]
    credit_method: Mapped[Optional[str]]

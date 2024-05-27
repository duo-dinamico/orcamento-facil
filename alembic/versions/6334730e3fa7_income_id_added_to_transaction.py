"""income id added to transaction

Revision ID: 6334730e3fa7
Revises: 3f195dae23de
Create Date: 2024-05-25 12:40:58.621008

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6334730e3fa7"
down_revision: Union[str, None] = "3f195dae23de"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    if op.get_bind().dialect.name == "sqlite":
        # Create new table with the desired schema and check constraint
        op.create_table(
            "new_transactions",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("account_id", sa.Integer(), nullable=False),
            sa.Column("subcategory_id", sa.Integer(), nullable=True, default=None),
            sa.Column("income_id", sa.Integer(), nullable=True, default=None),
            sa.Column(
                "transaction_type", sa.Enum("Income", "Expense", "Transfer", name="transactiontypeenum"), nullable=False
            ),
            sa.Column("value", sa.Integer(), nullable=False),
            sa.Column("currency_id", sa.Integer(), nullable=False),
            sa.Column("date", sa.DateTime(), nullable=False),
            sa.Column("description", sa.String(), nullable=True),
            sa.Column("target_account_id", sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(
                ["account_id"],
                ["accounts.id"],
            ),
            sa.ForeignKeyConstraint(["currency_id"], ["currencies.id"], name="currency"),
            sa.ForeignKeyConstraint(["subcategory_id"], ["subcategories.id"], name="subcategory"),
            sa.ForeignKeyConstraint(
                ["target_account_id"],
                ["accounts.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
            sa.CheckConstraint(
                "(subcategory_id IS NOT NULL AND income_id IS NULL) OR (subcategory_id IS NULL AND income_id IS NOT NULL)",
                name="check_subcategory_or_income",
            ),
        )

        # Copy data from old table to new table
        op.execute(
            """
            INSERT INTO new_transactions (
                id, account_id, subcategory_id, transaction_type, value, currency_id,
                date, description, target_account_id
            )
            SELECT
                id, account_id, subcategory_id, transaction_type, value, currency_id,
                date, description, target_account_id
            FROM transactions
        """
        )

        # Drop the old table and rename the new table to the old table name
        op.drop_table("transactions")
        op.rename_table("new_transactions", "transactions")
    else:
        # Non-SQLite databases can use standard SQL
        op.add_column("transactions", sa.Column("income_id", sa.Integer(), nullable=True))
        op.create_foreign_key("income", "transactions", "incomes", ["income_id"], ["id"])
        op.create_check_constraint(
            "check_subcategory_or_income",
            "transactions",
            "(subcategory_id IS NOT NULL AND income_id IS NULL) OR (subcategory_id IS NULL AND income_id IS NOT NULL)",
        )


def downgrade() -> None:
    if op.get_bind().dialect.name == "sqlite":
        # Steps to handle SQLite's limitations
        op.create_table(
            "old_transactions",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("account_id", sa.Integer(), nullable=False),
            sa.Column("subcategory_id", sa.Integer(), nullable=True, default=None),
            sa.Column("income_id", sa.Integer(), nullable=True, default=None),
            sa.Column(
                "transaction_type", sa.Enum("Income", "Expense", "Transfer", name="transactiontypeenum"), nullable=False
            ),
            sa.Column("value", sa.Integer(), nullable=False),
            sa.Column("currency_id", sa.Integer(), nullable=False),
            sa.Column("date", sa.DateTime(), nullable=False),
            sa.Column("description", sa.String(), nullable=True),
            sa.Column("target_account_id", sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(
                ["account_id"],
                ["accounts.id"],
            ),
            sa.ForeignKeyConstraint(["currency_id"], ["currencies.id"], name="currency"),
            sa.ForeignKeyConstraint(["subcategory_id"], ["subcategories.id"], name="subcategory"),
            sa.ForeignKeyConstraint(
                ["target_account_id"],
                ["accounts.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
        )

        # Copy data from current table to old table
        op.execute(
            """
            INSERT INTO old_transactions (
                id, account_id, subcategory_id, transaction_type, value, currency_id,
                date, description, target_account_id
            )
            SELECT
                id, account_id, subcategory_id, transaction_type, value, currency_id,
                date, description, target_account_id
            FROM transactions
        """
        )

        # Drop the current table and rename the old table to the current table name
        op.drop_table("transactions")
        op.rename_table("old_transactions", "transactions")
    else:
        # Non-SQLite databases can use standard SQL
        op.drop_constraint("check_subcategory_or_income", "transactions", type_="check")
        op.drop_constraint("income", "transactions", type_="foreignkey")
        op.drop_column("transactions", "income_id")

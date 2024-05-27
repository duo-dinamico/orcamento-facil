from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from ezbudget.model.base_models import Currency


class ModelCurrency:
    def __init__(self, parent_model):
        self.parent = parent_model

    def create_currency(self, name: str, symbol: str, code: str, symbol_position: str) -> Currency | str:
        """Create a new currency in the database and return a Category.

        Args:
            name: the name of the currency, that must be unique.
            symbol: the symbol of the currency, that must be unique.
            code: the code of the currency, that must be unique.
            symbol_position: the position of the symbol [prefix or suffix]

        Returns:
            Category: if a new category was created
            str: if it errors
        """
        try:
            new_currency = Currency(
                name=name,
                symbol=symbol,
                code=code,
                symbol_position=symbol_position,
            )

            self.parent.session.add(new_currency)
            self.parent.session.commit()
            self.parent.session.refresh(new_currency)
            return new_currency
        except IntegrityError as e:
            self.parent.session.rollback()
            if "unique constraint" in str(e.orig).lower():
                return "Name, symbol and code must all be unique"
            elif "not null constraint failed" in str(e.orig).lower():
                return "Name, symbol, code and symbol position are mandatory fields and cannot be empty"
            else:
                return "An unknown IntegrityError occurred"
        except LookupError as lookup_error:
            self.parent.session.rollback()
            return f"A LookupError occurred: {lookup_error}"

    def read_currencies(self) -> list:
        """Return a list of all currencies.

        Returns:
            [Currency]: list of all currencies.
        """
        return self.parent.read_all_basequery(select(Currency))

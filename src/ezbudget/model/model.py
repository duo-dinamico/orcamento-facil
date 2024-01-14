from typing import Optional

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.query import Query
from sqlalchemy.sql.expression import ScalarSelect

from ezbudget.model import Base
from ezbudget.model.model_account import ModelAccount
from ezbudget.model.model_category import ModelCategory
from ezbudget.model.model_income import ModelIncome
from ezbudget.model.model_subcategory import ModelSubCategory
from ezbudget.model.model_transaction import ModelTransaction
from ezbudget.model.model_user import ModelUser
from ezbudget.model.model_user_subcategory import ModelUserSubCategory
from ezbudget.presenter import ModelProtocol


class Model(ModelProtocol):
    def __init__(self, category_data, database_name: str = "of") -> None:
        self.engine = create_engine(f"sqlite:///{database_name}.db")
        # Composition
        self.model_account = ModelAccount(self)
        self.model_category = ModelCategory(self)
        self.model_income = ModelIncome(self)
        self.model_subcategory = ModelSubCategory(self)
        self.model_transaction = ModelTransaction(self)
        self.model_user_subcategory = ModelUserSubCategory(self)
        self.model_user = ModelUser(self)
        self._category_data = category_data

        @event.listens_for(self.engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            _ = connection_record
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON;")
            cursor.close()

        session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        Base.metadata.create_all(self.engine)
        self.session = session_local()

        if database_name == "of":
            self.populate_categories()

        self.user = None

    def populate_categories(self):
        if len(self.model_category.read_categories()) < 1:
            for item in self._category_data["categories"]:
                self.model_category.create_category(**item)
        if len(self.model_subcategory.read_subcategories()) < 1:
            for item in self._category_data["subcategories"]:
                self.model_subcategory.create_subcategory(**item)

    def close_session(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)

    # GENERIC METHODS
    def read_first_basequery(self, query: Query) -> Optional[ScalarSelect]:
        """Return a SQLAlchemy query selection that matches the given query.

        Args:
            query: SQLAlchemy query object

        Returns:
            ScalarSelect: the result of the selection
        """
        return self.session.scalars(query).first()

    def read_all_basequery(self, query: Query) -> Optional[ScalarSelect]:
        """Return a SQLAlchemy query selection that matches the given query.

        Args:
            query: SQLAlchemy query object

        Returns:
            ScalarSelect: the lest with results of the selection

        """
        return self.session.scalars(query).all()

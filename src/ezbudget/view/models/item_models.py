from PySide6.QtCore import QDateTime


class CategoryItem:
    def __init__(self, name, id, parent=None):
        self.name = name
        self._id = id
        self.parentItem = parent
        self.childItems = []

    def addChild(self, item):
        self.childItems.append(item)

    def children(self):
        return self.childItems

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return self.parentItem.rootItems.index(self) if self.parentItem else 0

    def data(self):
        return self.name

    def id(self):
        return self._id


class UserCategoryItem:
    def __init__(self, name, id):
        self.name = name
        self._id = id

    def data(self):
        return self.name

    def id(self):
        return self._id


class TransactionItem:
    def __init__(self, transaction):
        self._id = transaction.id
        self.account_id = transaction.account_id
        self.account_name = transaction.account.name
        self.category_name = transaction.subcategory.category.name
        self.subcategory_name = transaction.subcategory.name
        self._date = transaction.date
        self.transaction_type = transaction.transaction_type
        self.currency = transaction.currency
        self._value = transaction.value
        self.description = transaction.description
        self.target_account_id = transaction.target_account_id

    def category(self):
        return f"{self.category_name} - {self.subcategory_name}"

    def date(self):
        date_time = QDateTime.fromString(str(self._date), "yyyy-MM-dd hh:mm:ss")
        return date_time.toString("dd/MM/yyyy")

    def valueWithCurrency(self):
        return f"{self.currencySymbol()} {self.value()}"

    def value(self):
        return self._value / 100

    def currencySymbol(self):
        return self.currency.symbol

    def currencyName(self):
        return self.currency.name

    def transactionTypeValue(self):
        return self.transaction_type.value

    def transactionTypeName(self):
        return self.transaction_type.name

    def id(self):
        return self._id

    def accountId(self):
        return self.account_id

    def targetAccountId(self):
        return self.target_account_id


class CurrencyItem:
    def __init__(self, currency, value: float = 0.00):
        self._id = currency.id
        self.name = currency.name
        self.symbol = currency.symbol
        self.code = currency.code
        self.symbol_position = currency.symbol_position
        self.value = value

    def valueWithCurrency(self):
        value_with_currency = (
            f"{self.symbol} {self.value}" if self.symbol_position == "prefix" else f"{self.value} {self.symbol}"
        )
        return value_with_currency

    def getName(self):
        return self.name

    def getSymbol(self):
        return self.symbol

    def getId(self):
        return self._id

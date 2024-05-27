from PySide6.QtCore import (
    QAbstractItemModel,
    QAbstractListModel,
    QAbstractTableModel,
    QModelIndex,
    Qt,
    Signal,
)


class AbstractListModel(QAbstractListModel):
    def __init__(self, item_list=None):
        super().__init__()
        self.item_list: list = item_list or []

    def rowCount(self, _):
        return len(self.item_list)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            item = self.item_list[index.row()]
            return item.getName()

    def index(self, row, column, parent=QModelIndex()):
        if 0 <= row < self.rowCount(parent) and column == 0:
            return self.createIndex(row, column, self.item_list[row])
        return QModelIndex()

    def parent(self, index):
        return QModelIndex()

    def addListItem(self, item):
        self.beginInsertRows(QModelIndex(), len(self.item_list), len(self.item_list))
        self.item_list.append(item)
        self.item_list.sort(key=lambda item: item.getName())
        self.endInsertRows()

    def removeListItem(self, item_index: QModelIndex):
        row = item_index.row()
        if row < 0 or row >= len(self.item_list):
            return

        self.beginRemoveRows(QModelIndex(), row, row)
        del self.item_list[row]
        self.endRemoveRows()

    def setObjects(self, item_list):
        self.beginResetModel()
        self.item_list = item_list
        self.item_list.sort(key=lambda item: item.getName())
        self.endResetModel()


class CategoryModel(QAbstractItemModel):
    categoryInserted = Signal(QModelIndex)
    subCategoryInserted = Signal(QModelIndex)

    def __init__(self, rootItems=None, parent=None):
        super().__init__(parent)
        self.rootItems = rootItems if rootItems else []

    def getRootItemIndex(self, item):
        return self.rootItems.index(item) if item in self.rootItems else -1

    def index(self, row, column, parent=QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = None
        else:
            parentItem = parent.internalPointer()

        if parentItem:
            childItems = parentItem.children()
            if row < 0 or row >= len(childItems):
                return QModelIndex()
            childItem = childItems[row]
            return self.createIndex(row, column, childItem)
        else:
            if row < 0 or row >= len(self.rootItems):
                return QModelIndex()
            return self.createIndex(row, column, self.rootItems[row])

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem is None:
            # If the parent is None, it means the childItem is a root item
            return QModelIndex()
        return self.createIndex(self.getRootItemIndex(parentItem), 0, parentItem)

    def rowCount(self, parent=QModelIndex()):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = None
        else:
            parentItem = parent.internalPointer()

        if parentItem:
            return len(parentItem.children())
        else:  # If parent is root and asking for row count of root
            return len(self.rootItems)

    def columnCount(self, parent=QModelIndex()):
        return 1

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            item = index.internalPointer()
            return item.getName()  # Return the data of the item associated with the QModelIndex

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return "Category List"

    def addCategory(self, category):
        self.beginInsertRows(QModelIndex(), len(self.rootItems), len(self.rootItems))
        self.rootItems.append(category)
        self.endInsertRows()

        newIndex = self.index(len(self.rootItems) - 1, 0)
        self.categoryInserted.emit(newIndex)

    def addSubcategory(self, parent_item, subcategory_item):
        parent_index = self.index(self.getRootItemIndex(parent_item), 0, QModelIndex())
        self.beginInsertRows(parent_index, len(parent_item.children()), len(parent_item.children()))
        parent_item.addChild(subcategory_item)
        self.endInsertRows()

        newIndex = self.index(self.getRootItemIndex(parent_item), 0, parent_index)
        self.subCategoryInserted.emit(newIndex)

    def getCategories(self):
        response = []
        for item in self.rootItems:
            response.append(item)
        return response


class TableModel(QAbstractTableModel):
    def __init__(self, transactions):
        super().__init__()
        self.transactions = transactions
        self.headers = ["Account", "Category", "Date", "Type", "Value", "Description"]

    def rowCount(self, parent=QModelIndex()):
        return len(self.transactions)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        row_data = self.transactions[index.row()]
        if role == Qt.DisplayRole:
            if index.column() == 0:  # Account column
                return row_data.account_name
            elif index.column() == 1:  # Category column
                return row_data.category()
            elif index.column() == 2:  # Date column
                return row_data.date()
            elif index.column() == 3:  # Transaction type column
                return row_data.transactionTypeName()
            elif index.column() == 4:  # Value column
                return row_data.valueWithCurrency()
            elif index.column() == 5:  # Description column
                return row_data.description
        elif role == Qt.UserRole:  # Storing transaction ID in UserRole
            return row_data.id

    def index(self, row, column, parent=QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if parent.isValid():
            return QModelIndex()  # No support for hierarchical data, so return invalid index

        if 0 <= row < len(self.transactions) and 0 <= column < self.columnCount():
            item = self.transactions[row]
            return self.createIndex(row, column, item)  # Create QModelIndex with internal pointer to item
        else:
            return QModelIndex()  # Return invalid index if row or column is out of range

    def parent(self, index):
        return QModelIndex()

    def addTransaction(self, transaction_data):
        self.beginInsertRows(QModelIndex(), len(self.transactions), len(self.transactions))
        self.transactions.append(transaction_data)
        self.endInsertRows()

    def findItemRow(self, item):
        for row, data_item in enumerate(self.transactions):
            if data_item == item:
                return row
        return -1  # Item not found

    def updateTransaction(self, item, updated_item):
        row = self.findItemRow(item)
        if row < 0 or row >= len(self.transactions):
            return

        transaction_index = self.index(row, 0)
        self.transactions[row] = updated_item

        self.dataChanged.emit(transaction_index, transaction_index)

    def removeTransaction(self, item):
        row = self.findItemRow(item)
        if row < 0 or row >= len(self.transactions):
            return

        self.beginRemoveRows(QModelIndex(), row, row)
        del self.transactions[row]
        self.endRemoveRows()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]

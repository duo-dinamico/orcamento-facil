from tkinter import ttk

categories = [
    {"id": 1, "name": "house"},
    {"id": 2, "name": "entertainment"},
    {"id": 3, "name": "utilities"},
    {"id": 4, "name": "transportation"},
]

subcategories = [
    {"id": 1, "category_id": 1, "name": "house 1", "recurrent": True, "recurrence": "MONTH", "include": True},
    {"id": 2, "category_id": 1, "name": "house 2", "recurrent": False, "recurrence": "ONE", "include": True},
    {"id": 3, "category_id": 3, "name": "utilities 1", "recurrent": True, "recurrence": "YEAR", "include": True},
]


class Categories(ttk.Frame):
    def __init__(self, parent, presenter) -> None:
        super().__init__(master=parent)
        style = ttk.Style()
        style.configure("Treeview", font=(None, 11), rowheight=int(11 * 3))

        self.tree = ttk.Treeview(self)
        self.tree.heading("#0", text="Categories", anchor="w")

        for category in categories:
            self.tree.insert("", "end", text=category["name"], iid=category["id"], open=False)

        for subcategory in subcategories:
            subcategory_index = subcategory["id"] + len(categories)
            self.tree.insert("", "end", text=subcategory["name"], iid=subcategory_index, open=False)
            self.tree.move(item=subcategory_index, parent=subcategory["category_id"], index=subcategory_index)

        self.tree.pack(fill="both", expand=True)

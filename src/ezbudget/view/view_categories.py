import ttkbootstrap as ttk

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

        lbl_instructions = ttk.Label(
            self,
            text="Click on subcategories to select or click categories to select all subcategories. Press arrow button to move into selected categories.",
        )
        lbl_instructions.pack(fill="x", expand=True, padx=10, pady=(10, 0))

        tvw_categories = ttk.Treeview(self, selectmode="none")
        tvw_categories.heading("#0", text="Categories", anchor="w")
        for category in categories:
            tvw_categories.insert("", "end", text=category["name"], iid=category["id"], open=False, tags="parent")
        for subcategory in subcategories:
            subcategory_index = subcategory["id"] + len(categories)
            tvw_categories.insert(
                "", "end", text=subcategory["name"], iid=subcategory_index, open=False, tags="selectable"
            )
            tvw_categories.move(item=subcategory_index, parent=subcategory["category_id"], index=subcategory_index)
        tvw_categories.pack(fill="both", expand=True, padx=10, pady=10)
        tvw_categories.bind("<Button-1>", self.enable_selection)

    def enable_selection(self, event):
        tree = event.widget
        item_name = tree.identify_row(event.y)
        if item_name:
            tags = tree.item(item_name, "tags")
            if tags and (tags[0] == "selectable"):
                tree.selection_set(item_name)
            elif tags and (tags[0] == "parent"):
                tree.item(item_name, open=True)
                selection = tree.get_children(item_name)
                tree.selection_set(selection)

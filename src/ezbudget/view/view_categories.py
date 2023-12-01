import tkinter as tk
from tkinter import messagebox

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
        self.presenter = presenter
        style = ttk.Style()
        style.configure("Treeview", font=(None, 11), rowheight=int(11 * 3))

        txt_instructions = tk.Text(self, height=2)
        txt_instructions.insert(
            "end", "Click on subcategories to select or click categories to select all subcategories."
        )
        txt_instructions.insert("end", "\nPress arrow button to move into selected categories.")
        txt_instructions["state"] = "disabled"
        txt_instructions.pack(fill="x", padx=10, pady=(10, 0))

        self.tvw_categories = ttk.Treeview(self, selectmode="none", bootstyle="primary")
        self.tvw_categories.heading("#0", text="Categories", anchor="w")

        self.tvw_categories.pack(fill="both", expand=True, padx=10, pady=10, side="left")
        self.tvw_categories.bind("<Button-1>", self.enable_selection)

        frm_buttons = ttk.Frame(self)
        frm_buttons.pack(padx=10, pady=10, side="left")

        btn_move_selected = ttk.Button(frm_buttons, text=">>", bootstyle="primary")
        btn_move_selected.pack(padx=10, pady=10)
        btn_move_selected.bind("<Button-1>", self.move_selected)
        btn_remove_selected = ttk.Button(frm_buttons, text="<<", bootstyle="primary")
        btn_remove_selected.pack(padx=10, pady=10)
        btn_remove_selected.bind("<Button-1>", self.remove_selected)

        self.tvw_selected_categories = ttk.Treeview(self, bootstyle="primary", selectmode="extended")
        self.tvw_selected_categories.heading("#0", text="Selected categories", anchor="w")
        self.tvw_selected_categories.pack(fill="both", expand=True, padx=10, pady=10, side="left")

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
                tree.selection_set(selection)

    def move_selected(self, event):
        del event
        items = self.tvw_categories.selection()
        caught_errors = []
        for item in items:
            subcategory_index = int(item) - len(categories)
            try:
                self.presenter.handle_add_user_category()
                self.tvw_selected_categories.insert(
                    "", "end", iid=subcategory_index, text=self.tvw_categories.item(item)["text"]
                )
            except tk.TclError as e:
                # TODO in the future we should log this error for tracking
                del e
                caught_errors.append(f'{self.tvw_categories.item(item)["text"]} already selected')

        if len(caught_errors) > 0:
            error_message = "\n".join(caught_errors)
            caught_errors = []
            # TODO replace with ttk toplevel?
            messagebox.showinfo(title="Information", message=error_message)

    def remove_selected(self, event):
        del event
        items = self.tvw_selected_categories.selection()
        for item in items:
            self.tvw_selected_categories.delete(item)

    def refresh_categories(self):
        category_list = self.presenter.refresh_category_list()
        subcategory_list = self.presenter.refresh_subcategory_list()
        for category in category_list:
            self.tvw_categories.insert("", "end", text=category.name, iid=category.id, open=False, tags="parent")
        for subcategory in subcategory_list:
            subcategory_index = subcategory.id + len(category_list)
            self.tvw_categories.insert(
                "", "end", text=subcategory.name, iid=subcategory_index, open=False, tags="selectable"
            )
            self.tvw_categories.move(item=subcategory_index, parent=subcategory.category_id, index=subcategory_index)

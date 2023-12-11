import tkinter as tk

import ttkbootstrap as ttk


class Categories(ttk.Frame):
    def __init__(self, parent, presenter) -> None:
        super().__init__(master=parent, bootstyle="secondary")
        self.parent = parent
        self.presenter = presenter

        txt_instructions = tk.Text(self, height=2, font=("Roboto", 14, "bold"))
        txt_instructions.insert(
            "end", "Click on subcategories to select or click categories to select all subcategories."
        )
        txt_instructions.insert("end", "\nPress arrow button to move into selected categories.")
        txt_instructions["state"] = "disabled"
        txt_instructions.pack(fill="x", padx=10, pady=(10, 0))

        frm_treeviews = ttk.Frame(self, bootstyle="secondary")
        frm_treeviews.pack(fill="both", expand=True, padx=10, pady=10)

        self.tvw_categories = ttk.Treeview(frm_treeviews, selectmode="none", bootstyle="light")
        self.tvw_categories.heading("#0", text="Categories", anchor="w")
        self.tvw_categories.pack(fill="both", expand=True, pady=10, side="left")
        self.tvw_categories.bind("<Button-1>", self.enable_selection)

        frm_buttons = ttk.Frame(frm_treeviews, bootstyle="secondary")
        frm_buttons.pack(padx=10, pady=10, side="left")

        btn_move_selected = ttk.Button(frm_buttons, text=">>", style="TButton", bootstyle="dark")
        btn_move_selected.pack(padx=10, pady=10)
        btn_move_selected.bind("<Button-1>", self.move_selected)
        btn_remove_selected = ttk.Button(frm_buttons, text="<<", style="TButton", bootstyle="dark")
        btn_remove_selected.pack(padx=10, pady=10)
        btn_remove_selected.bind("<Button-1>", self.remove_selected)

        self.tvw_selected_categories = ttk.Treeview(frm_treeviews, bootstyle="light", selectmode="extended")
        self.tvw_selected_categories.heading("#0", text="Selected categories", anchor="w")
        self.tvw_selected_categories.pack(fill="both", expand=True, pady=10, side="left")

        btn_show_homepage = ttk.Button(master=self, text="Return to Homepage")
        btn_show_homepage.pack(padx=10, pady=(0, 10), side="bottom", fill="x")
        btn_show_homepage.bind("<Button-1>", self.parent.show_homepage)

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
        for item in items:
            self.presenter.handle_add_user_category(subcategory_id=item.split(" ")[1])
        self.refresh_selected_categories()

    def remove_selected(self, event):
        del event
        items = self.tvw_selected_categories.selection()
        for item in items:
            self.presenter.handle_remove_user_category(subcategory_id=item.split(" ")[1])
        self.refresh_selected_categories()

    def refresh_categories(self):
        category_list = self.presenter.refresh_category_list()
        subcategory_list = self.presenter.refresh_subcategory_list()
        for category in category_list:
            self.tvw_categories.insert(
                "", "end", text=category.name, iid=f"category {category.id}", open=False, tags="parent"
            )
        for subcategory in subcategory_list:
            self.tvw_categories.insert(
                "", "end", text=subcategory.name, iid=f"subcategory {subcategory.id}", open=False, tags="selectable"
            )
            self.tvw_categories.move(
                item=f"subcategory {subcategory.id}", parent=f"category {subcategory.category_id}", index=subcategory.id
            )

    def refresh_selected_categories(self):
        for item in self.tvw_selected_categories.get_children():
            self.tvw_selected_categories.delete(item)

        selected_categories = self.presenter.refresh_selected_category_list()
        for category in selected_categories:
            self.tvw_selected_categories.insert(
                "", "end", iid=f"subcategory {category.subcategory_id}", text=category.subcategory.name
            )

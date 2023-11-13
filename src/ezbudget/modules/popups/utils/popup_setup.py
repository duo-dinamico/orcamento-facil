def popup_setup(self, parent, title):
    self.grab_set()
    self.transient(parent)
    self.resizable(False, False)
    self.title(title)

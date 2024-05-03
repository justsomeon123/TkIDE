from tkinter import Entry, Label, Toplevel, ttk

from source.tabs import Tab


class SettingsPage(Tab):
    def __init__(self, master, title, **kwargs) -> None:
        super().__init__(master, title, **kwargs)


main = lambda master:SettingsPage(master,"Settings")
import platform
import tkinter as tk
def FullScreen(root):
    x = platform.system()
    if x == "Windows":
        root.state('zoomed')
    if x == "Linux":
        root.attributes('-zoomed', True)
    if x == "OSX":
        root.state('zoomed')
import platform
def FullScreen(root) -> str:
    x = platform.system()
    if x == "Windows":
        root.state('zoomed')
    if x == "Linux":
        root.attributes('-zoomed', True)
    if x == "OSX":
        root.state('zoomed')
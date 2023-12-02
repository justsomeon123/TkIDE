"""Important functions seperated from the main file."""
import platform

def FullScreen(root) -> None: 
    os = platform.system()
    if os == "Windows" or "OSX":
        root.state('zoomed')
    if os == "Linux":
        root.attributes('-zoomed', True)
    else:
        return None

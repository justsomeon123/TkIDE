import platform
from source.CustomClasses import IDEText,END
from pygments import lex
import pygments.lexers as lexers


#adapted from stackoverflow https://stackoverflow.com/questions/32058760/improve-pygments-syntax-highlighting-speed-for-tkinter-text
def highlight(Display:IDEText):
    Display.content = Display.get("1.0", END)
    Display.lines = Display.content.split("\n")
    Display.previousContent = ""
    
    lexer = lexers.get_lexer_for_filename(Display.filename)

    if (Display.previousContent != Display.content):
        Display.row = Display.index("insert").split(".")[0]
        Display.mark_set("range_start", Display.row + ".0")
        data = Display.get(Display.row + ".0", Display.row + "." + str(len(Display.lines[int(Display.row) - 1])))

        for token, content in lex(data, lexer):
            Display.mark_set("range_end", "range_start + %dc" % len(content))
            Display.tag_add(str(token), "range_start", "range_end")
            Display.mark_set("range_start", "range_end")

    Display.previousContent = Display.get("1.0", END)


def FullScreen(root) -> None: 
    os = platform.system()
    if os == "Windows" or "OSX":
        root.state('zoomed')
    if os == "Linux":
        root.attributes('-zoomed', True)
    else:
        return None

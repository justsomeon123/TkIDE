import platform
from source.CustomClasses import IDEText,END
from pygments import lex
import pygments.lexers as lexers


def PythonHighlight(Display:IDEText):
    Display.tag_configure("Token.Comment", foreground="#b21111")
    print(lexers.get_lexer_for_filename(Display.filename))
    Display.mark_set("range_start", "1.0")
    data = Display.get("1.0", "end-1c")
    for token, content in lex(data, lexers.get_lexer_for_filename(Display.filename)):
        Display.mark_set("range_end", "range_start + %dc" % len(content))
        Display.tag_add(str(token), "range_start", "range_end")
        Display.mark_set("range_start", "range_end")    

    


def FullScreen(root) -> None: 
    x = platform.system()
    if x == "Windows" or "OSX":
        root.state('zoomed')
    if x == "Linux":
        root.attributes('-zoomed', True)
    else:
        return None

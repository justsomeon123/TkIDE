"""Some important functions, mostly just the highlighting function"""
import platform
from source.CustomClasses import IDEText
from pygments import lex
import pygments.lexers as lexers


#adapted from stackoverflow https://stackoverflow.com/questions/32058760/improve-pygments-syntax-highlighting-speed-for-tkinter-text
def highlight(Display:IDEText):
    Display.mark_set("range_start", "1.0")
    _lex = lexers.get_lexer_for_filename(Display.filename)

    data = Display.get(Display.index("insert").split(".")[0]+".0",Display.index("insert").split(".")[0]+".end")
    for token, content in lex(data,_lex):
        try:
            print(token)
            start = Display.search(content,Display.index("insert").split(".")[0]+".0",Display.index("insert").split(".")[0]+".end")
            end = start.split(".")[0] + "." + str(int(start.split(".")[1]) + len(content))
            print(f"{start},{end}")

            Display.tag_add(str(token), start, end)
        except Exception:
            #very buggy code, so rather than crashing when unable to parse and hhighlight
            #simply ignore, and don't highlight any text
            pass



def FullScreen(root) -> None: 
    os = platform.system()
    if os == "Windows" or "OSX":
        root.state('zoomed')
    if os == "Linux":
        root.attributes('-zoomed', True)
    else:
        return None

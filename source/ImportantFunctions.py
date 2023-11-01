"""Important functions seperated from the main file."""
import platform
from source.CustomClasses import IDEText
from pygments import lex
import pygments.lexers as lexers


#adapted from stackoverflow https://stackoverflow.com/questions/32058760/improve-pygments-syntax-highlighting-speed-for-tkinter-text
def highlight(Display:IDEText):
    Display.mark_set("range_start", "1.0")
    _lex = lexers.get_lexer_for_filename(Display.filename)

    line_num = Display.index("insert").split(".")[0]
    line_bgn = line_num + ".0"
    line_end = line_num + ".end"

    data = Display.get(line_bgn,line_end)
    for token, content in lex(data,_lex):
        print(token)
        start = Display.search(content,line_bgn,line_end) #Finds the index at which the current token starts
        if not start:
            break
        print(start)
        end = line_num + "." + str(int(start.split(".")[1]) + len(content)) #Finds the end of the current token using the length of the token
        Display.tag_add(str(token), start, end)



def FullScreen(root) -> None: 
    os = platform.system()
    if os == "Windows" or "OSX":
        root.state('zoomed')
    if os == "Linux":
        root.attributes('-zoomed', True)
    else:
        return None

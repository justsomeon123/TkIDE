import platform
from source.CustomClasses import IDEText,END,keyword



def PythonHighlight(Display:IDEText,HighlightThemes):
    
    tags = list(HighlightThemes)
    for tag in tags:
        Display.tag_remove(tag,1.0,END)

    Display.tag_configure('default',foreground=HighlightThemes["default"])
    Display.tag_configure("intger",foreground=HighlightThemes["intger"])
    Display.tag_configure("string",foreground=HighlightThemes["string"])
    Display.tag_configure("keyword",foreground=HighlightThemes["keyword"])
    Display.tag_configure("comment",foreground=HighlightThemes["comment"])
    Display.tag_configure("operator",foreground=HighlightThemes["operator"])

    #adding tags to text

    #default
    pythonkeywords =  keyword.kwlist
    for i in pythonkeywords:
        i = ' ' + i + ' '
        Display.highlight_pattern(i,"keyword")
        i = ' ' + i + ':'
        Display.highlight_pattern(i,"keyword")
        i = '' + i + ' '
        Display.highlight_pattern(i,"keyword")
        i = ' ' + i + '\n'
        Display.highlight_pattern(i,"keyword")
        i = ' ' + i + '\t'
        Display.highlight_pattern(i,"keyword")

    #intgers
    for i in [1,2,3,4,5,6,7,8,9,0]:
        Display.highlight_pattern(str(i),"intger")

    #strings with regexp
    Display.highlight_pattern(r'"(.*?)\"',"string",regexp=True)
    Display.highlight_pattern(r"'(.*?)\'","string",regexp=True)
    Display.highlight_pattern(r"#(.*)","comment",regexp=True)
    


def FullScreen(root) -> None: 
    x = platform.system()
    x = "12"
    if x == "Windows" or "OSX":
        root.state('zoomed')
    if x == "Linux":
        root.attributes('-zoomed', True)
    else:
        return None

import tkinter
import tkinter.scrolledtext as ScrolledText
from pygments import lex
from pygments.lexers import PythonLexer

#slightly adapted from stackoverflow (lost the link) to test

root = tkinter.Tk()
textPad = ScrolledText.ScrolledText(root, width=100, height=80)
textPad.tag_configure("Token.Comment.Single", foreground="#aaaaaa")
textPad.tag_configure("Token.Literal.Number.Inteer", foreground="#aaaaaa")
code = textPad.get("1.0", "end-1c")
mylexer69420 = PythonLexer()


def syn(event=None):
    textPad.mark_set("range_start", "1.0")


    data = textPad.get(textPad.index("insert").split(".")[0]+".0",textPad.index("insert").split(".")[0]+".end")
    for token, content in lex(data,mylexer69420):
        print(token)
        textPad.tag_add(str(token), textPad.index("insert").split(".")[0]+".0",textPad.index("insert").split(".")[0]+".end")

textPad.pack()
root.bind("<KeyRelease>", syn)
root.mainloop()
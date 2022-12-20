#Most of the code here is from stackoverflow but modified to fit my needs.


from tkinter import Text,Tk,Label,Scrollbar,IntVar,Frame,LEFT,RIGHT,Y,NW,NE,BOTH,font,ttk,PhotoImage,Canvas,END #end is used in highlighting
import os

#Adapted from https://stackoverflow.com/questions/3781670/how-to-highlight-text-in-a-tkinter-text-widget?rq=1, https://stackoverflow.com/questions/32058760/improve-pygments-syntax-highlighting-speed-for-tkinter-text
class IDEText(Text):

    def __init__(self,*args, **kwargs):
        self.filename = kwargs["filename"] #ger the filename from the kwargs for pygments highlighting
        kwargs.pop("filename") # Make sure Text init doesn't get filename as an option
        Text.__init__(self, *args, **kwargs)
        self.tag_configure("Token.Keyword", foreground="#CC7A00")
        self.tag_configure("Token.Keyword.Constant", foreground="#CC7A00")
        self.tag_configure("Token.Keyword.Declaration", foreground="#CC7A00")
        self.tag_configure("Token.Keyword.Namespace", foreground="#CC7A00")
        self.tag_configure("Token.Keyword.Pseudo", foreground="#CC7A00")
        self.tag_configure("Token.Keyword.Reserved", foreground="#CC7A00")
        self.tag_configure("Token.Keyword.Type", foreground="#CC7A00")
        self.tag_configure("Token.Name.Class", foreground="#003D99")
        self.tag_configure("Token.Name.Exception", foreground="#003D99")
        self.tag_configure("Token.Name.Function", foreground="#003D99")
        self.tag_configure("Token.Operator", foreground="#CC7A00")
        self.tag_configure("Token.Literal.String.Single", foreground="#248F24")
        self.tag_configure("Token.Literal.Number.Integer", foreground="#fc8c03")
        self.tag_configure("Token.Comment.Single", foreground="#bbbbbb")
        self.tag_configure("Token.Literal.Boolean", foreground="#a3F133")

#for the first time, i am going to start this withot stackoverflow




#Adapted from https://stackoverflow.com/questions/39458337/is-there-a-way-to-add-close-buttons-to-tabs-in-tkinter-ttk-notebook

class CustomNotebook(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab"""

    __initialized = False

    def __init__(self,TabList,StringDict,*args, **kwargs):
        if not self.__initialized:
            self.__initialize_custom_style()
            self.__inititialized = True
        self.TabList:list = TabList
        self.StringDict:dict = StringDict

        kwargs["style"] = "CustomNotebook"
        ttk.Notebook.__init__(self, *args, **kwargs)

        self._active = None

        self.TabMoveframe = Frame(self)
        self.TabMoveframe.pack(anchor=NE)
        self.BackTabButton = Label(self.TabMoveframe,text="\u276E ",font=font.Font(size=14))
        self.FrontTabButton = Label(self.TabMoveframe,text="\u276F ",font=font.Font(size=14))
        self.TabMenuButton = Label(self.TabMoveframe,text="\u2630 ",font=font.Font(size=14))
        self.BackTabButton.grid(row=1,column=0)
        self.BackTabButton.bind('<Button-1>',lambda event:self.select(self.index(self.select())-1))
        self.FrontTabButton.grid(row=1,column=1)
        self.FrontTabButton.bind('<Button-1>',lambda event:self.select(self.index(self.select())+1))
        self.TabMenuButton.grid(row=1,column=2)

        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""

        element = self.identify(event.x, event.y)

        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(['pressed'])
            self._active = index
            return "break"

    def on_close_release(self, event):
        """Called when the button is released"""
        if not self.instate(['pressed']):
            return

        element =  self.identify(event.x, event.y)
        if "close" not in element:
            # user moved the mouse off of the close button
            return

        index = self.index("@%d,%d" % (event.x, event.y))

        if self._active == index:
            self.forget(index)
            self.StringDict.pop(self.TabList[index])
            self.TabList.pop(index)
            self.event_generate("<<NotebookTabClosed>>")

        self.state(["!pressed"])
        self._active = None
    
    def forceclose(self):
        index = self.se
        if self._active == index:
            self.forget(index)
            self.StringDict.pop(self.TabList[index])
            self.TabList.pop(index)
            self.event_generate("<<NotebookTabClosed>>")

    def __initialize_custom_style(self):
        style = ttk.Style()
        self.images = (
            PhotoImage("img_close", data='''
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                '''),
            PhotoImage("img_closeactive", data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                '''),
            PhotoImage("img_closepressed", data='''
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            ''')
        )

        style.element_create("close", "image", "img_close",
                            ("active", "pressed", "!disabled", "img_closepressed"),
                            ("active", "!disabled", "img_closeactive"), border=8, sticky='')
        style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": "nswe"})])
        style.layout("CustomNotebook.Tab", [
            ("CustomNotebook.tab", {
                "sticky": "nswe",
                "children": [
                    ("CustomNotebook.padding", {
                        "side": "top",
                        "sticky": "nswe",
                        "children": [
                            ("CustomNotebook.focus", {
                                "side": "top",
                                "sticky": "nswe",
                                "children": [
                                    ("CustomNotebook.label", {"side": "left", "sticky": ''}),
                                    ("CustomNotebook.close", {"side": "left", "sticky": ''}),
                                ]
                        })
                    ]
                })
            ]
        })
    ])

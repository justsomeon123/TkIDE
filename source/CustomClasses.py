from tkinter import Text,Tk,Label,Scrollbar,IntVar,Frame,LEFT,RIGHT,Y,NW,NE,BOTH,font,ttk,PhotoImage,Canvas,END #end is used in highlighting
import os,keyword
class IDEText(Text):
    '''A text widget with a new method, highlight_pattern()

    example:

    text = CustomText()
    text.tag_configure("red", foreground="#ff0000")
    text.highlight_pattern("this should be red", "red")

    The highlight_pattern method is a simplified python
    version of the tcl code at http://wiki.tcl.tk/3246
    '''
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)

    def highlight_pattern(self, pattern, tag, start="1.0", end="end",
                          regexp=False):
        '''Apply the given tag to all text that matches the given pattern

        If 'regexp' is set to True, pattern will be treated as a regular
        expression according to Tcl's regular expression syntax.
        '''

        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)

        count = IntVar()
        while True:
            index = self.search(pattern, "matchEnd","searchLimit",
                                count=count, regexp=regexp)
            if index == "": break
            if count.get() == 0: break # degenerate pattern which matches zero-length strings
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")


    
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


class TreeviewFrame(object):
    def __init__(self, master, path):
        self.nodes = dict()
        frame = Frame(master)
        self.tree = ttk.Treeview(frame)
        ysb = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
        xsb = ttk.Scrollbar(frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.tree.heading('#0', text='', anchor='w')

        ysb.pack(side='right', fill='y')
        xsb.pack(side='bottom', fill='x')
        self.tree.pack(side=LEFT, fill=BOTH)
        frame.pack(side=LEFT, fill=Y)

        abspath = os.path.abspath(path)
        self.insert_node('', abspath, abspath)
        self.tree.bind('<<TreeviewOpen>>', self.open_node)
        ttk.Sizegrip(self.tree).place(relx=1.0, rely=1.0, anchor='se')
        
    def LoadNewFolder(self,path):
        abspath = os.path.abspath(path)
        self.tree.delete(*self.tree.get_children())
        self.insert_node('', abspath, abspath)
        
        
    
    def insert_node(self, parent, text, abspath):
        node = self.tree.insert(parent, 'end', text=text, open=False)
        if os.path.isdir(abspath):
            self.nodes[node] = abspath
            self.tree.insert(node, 'end')

    def open_node(self, event):
        node = self.tree.focus()
        abspath = self.nodes.pop(node, None)
        if abspath:
            self.tree.delete(self.tree.get_children(node))
            for p in os.listdir(abspath):
                self.tree.bind("<<TreeviewSelect>>", self.print_element)
                self.insert_node(node, p, os.path.join(abspath, p))
    
    def print_element(self,event):
        tree = event.widget
        selection = [tree.item(item)["abspath"] for item in tree.selection()]
        print("selected items:", selection)

def PythonHighlight(Display:IDEText,HighlightThemes):
    tags = list(HighlightThemes)
    for tag in tags:
        Display.tag_remove(tag,1.0,END)

    Display.tag_configure('default',foreground=HighlightThemes["default"])
    Display.tag_configure("intger",foreground=HighlightThemes["intger"])
    Display.tag_configure("string",foreground=HighlightThemes["string"])
    Display.tag_configure("keyword",foreground=HighlightThemes["keyword"])
    Display.tag_configure("comment",foreground=HighlightThemes["comment"])

    #adding tags to text

    #default
    pythonkeywords =  keyword.kwlist
    for i in pythonkeywords:
        i = ' ' + i + ' '
        Display.highlight_pattern(i,"keyword")
        i = ' ' + i + ':'
        Display.highlight_pattern(i,"keyword")

    #intgers
    for i in [1,2,3,4,5,6,7,8,9,0]:
        Display.highlight_pattern(str(i),"intger")

    #strings with regexp
    Display.highlight_pattern(r'"(.*?)\"',"string",regexp=True)
    Display.highlight_pattern(r"'(.*?)\'","string",regexp=True)

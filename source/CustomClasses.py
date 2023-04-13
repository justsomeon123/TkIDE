"""Some code for classes like IDEText"""
#Most of the code here is adapted from stackoverflow to fit my needs.

import sys
from tkinter import Text,Label,Frame,NE,BOTH,font,ttk,PhotoImage,END,Toplevel,Scrollbar,Entry 
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


class FileSystemWidget(ttk.Frame):
    def __init__(self, master, path):
        super().__init__(master)

        self.treeview = ttk.Treeview(self, columns=("type",))
        self.treeview.heading("#0", text=path, anchor="w")
        self.treeview.column("#0", width=300)
        self.treeview.column("type", width=50)
        self.treeview.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

        self.populate_treeview(path)

    def populate_treeview(self, path, parent=""):
        for filename in os.listdir(path):
            full_path = os.path.join(path, filename)
            truncated_filename = filename[:25] + "..." if len(filename) > 25 else filename
            item = self.treeview.insert(parent, "end", text=truncated_filename, values=(self.get_filetype(full_path),))
            if os.path.isdir(full_path):
                self.populate_treeview(full_path, parent=item)

    def get_filetype(self, path):
        if os.path.isdir(path):
            return "dir"
        else:
            return "file"


class TerminalWindow:
    def __init__(self,zehigherone):
        self.root = Toplevel()
        self.parent = zehigherone
        self.root.title('Run Output')
        self.text = Text(self.root)
        self.text.pack(expand=True, fill=BOTH)
        
        # create a scroll bar and attach it to the text widget
        scroll = Scrollbar(self.root)
        scroll.pack(side='right', fill='y')
        scroll.config(command=self.text.yview)
        self.text.config(yscrollcommand=scroll.set)
        
        # create an entry widget to take user input
        self.entry = Entry(self.root)
        self.entry.pack(side='bottom', fill='x')
        self.entry.bind('<Return>', self.on_return)
        
        self.text.insert(END, ">>> ")
        
    def on_return(self, event):
        # get the user input and process it
        user_input = self.entry.get()
        self.text.insert(END, user_input + '\n')
        self.entry.delete(0, END)
        self.process_command(user_input)
        self.text.insert(END, ">>> ")
        
    def process_command(self, command:str):
        if command == "forcequit":
            sys.exit(0)
        if command.startswith("newtab"):
            try:
                z = command.removeprefix("newtab").strip()
                self.parent.NewTab(z)
                self.text.insert(END,f"Created tab for file {z}\n")
            except IndexError:
                self.text.insert(END,f"Error, add a filename. Ex:newtab C:/Users/user/test.txt\n")
        else:
            self.text.insert(END, f"Error: command {command} not known \n")
        
    def run(self):
        self.root.mainloop()

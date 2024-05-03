#Version:2.7 Last Updated:2023-12-1
#Look at README.md for more information
#############################################################################################
#TkIDE.pyw


import json
import os
import platform
import random
import string
from tkinter import (BOTH, NW, Button, Event, Frame, Menu, Tk, filedialog,
                     messagebox, ttk,PhotoImage)

#Internal imports
import CustomClasses as cc
import extensions as ext_lib
import tabs
import term


class Editor:
    def __init__(self) -> None:
        #SECTION:Setup
        self.root = Tk()
        

        with open('./assets/settings.json') as f:
            self.settings = json.load(f)
        
        if self.settings["extensionsEnabled"]:
            if self.settings["experimentalExtensions"]:
                self.ext_mgr = ext_lib.ExtensionManager()
            else:
                self.ext_mgr = ext_lib.OldExtensionManager(self,self.settings)
            pass
            

        #SECTION:Icons 
        MainIcon = PhotoImage(file=self.settings["icon"])
        self.FileIcon = PhotoImage(file=self.settings["file-icon"])
        self.ImageIcon = PhotoImage(file=self.settings["image-icon"])

        #SECTION:Shortcuts
        self.root.bind('<Control-o>',lambda event:self.OpenFile())
        self.root.bind('<Control-n>',lambda event:self.CreateFile())
        self.root.bind('<Control-`>',lambda event:term.TerminalWindow())
        self.root.bind('<Control-p>',lambda event:self.TestEvent())

        #SECTION:Root Management        
        self.root.iconphoto(True,MainIcon)     
        self.root.title('TkIDE')

        pltfrm = platform.system()
        if pltfrm == "Windows" or "OSX":
            self.root.state('zoomed')
        if pltfrm == "Linux":
            self.root.attributes('-zoomed', True)
        else:
            pass


        #self.__settingsinit__()
        #SECTION:Menus  
        self.Menu = Menu(self.root)
        ##SUBSECTION:File Menu
        FileMenu = Menu(self.Menu,tearoff=0)
        FileMenu.add_command(label='Open File',command=lambda:self.OpenFile())
        FileMenu.add_command(label='Create a New File',command=lambda:self.CreateFile())
        FileMenu.add_command(label="Save",command=lambda:self.Save())
        FileMenu.add_separator(background="red")
        FileMenu.add_command(label="Delete a File",foreground="red",command=lambda:self.DeleteFile(),background="dark red")
        ##SUBSECTION:File Menu:END

        ##SUBSECTION:Terminal Menu
        TerminalMenu = Menu(self.Menu,tearoff=0)
        TerminalMenu.add_command(label='Terminal',command=lambda:term.TerminalWindow(self))
        ##SUBSECTION:Terminal Menu:END

        ##SUBSECTION:Menu adding
        self.Menu.add_cascade(label="File",menu=FileMenu)
        self.Menu.add_cascade(label="Terminal",menu=TerminalMenu)
        self.root.config(menu=self.Menu)
        ##SUBSECTION:Menu adding:END
        
        #SECTION:Main Editor
        self.TabCount = 0 #Tab count.
        self.Pages = {} #dictionary of pages/tabs and their key values
        self.TabIdentifiers = [] #Random strings that correspond to each page , look at self.RandomString() for more info.
        self.EditorPages = cc.CustomNotebook(self.TabIdentifiers,self.Pages) #the main editor interface. (View CustomClasses.CustomNotebook for more information)
        self.EditorPages.pack(expand=True,fill=BOTH)

        ##SECTION:Welcome Page
        tab_identifier = self.RandomString() #Creates a tab identifier for this tab.
        self.TabIdentifiers.append(tab_identifier) #Adds it to the storage of tab identifiers.
        self.Pages[tab_identifier]  = (ttk.Frame(self.EditorPages),"welcomepage") #Stores the informaton on each pages critical parts
        PageFrame = self.Pages[tab_identifier][0] #PageFrame is the Frame holding the editor/page content
        self.EditorPages.add(PageFrame, text=f"Home",image=MainIcon,compound="left") # Add a tab.
        ttk.Label(PageFrame,text="Press these buttons or use the menu at the top").pack(anchor=NW,pady=10) #Buttons on welcome page.
        ttk.Button(PageFrame,text="Open File",command=lambda:self.OpenFile()).pack(anchor=NW)
        ttk.Button(PageFrame,text="Create a New File",command=lambda:self.CreateFile()).pack(anchor=NW)
        ttk.Button(PageFrame,text="Delete a File",command=lambda:self.DeleteFileConfirm()).pack(anchor=NW)
        
        if not self.settings["enableHighlighting"]:
            messagebox.showinfo("Highlighting","Highlighting is disabled. Go to settings to enable it.")

        #SECTION:Loop
        self.root.mainloop() #Gui loop.
    
    def TestEvent(self):
        ttk.Style().configure("Bw.TLabel",bg="#aba89f")
        self.ext_mgr.LoadExtensionsFrom();self.ext_mgr.RunMains(self);

        menoo = Frame(self.root,background="#aba89f")
        menoo.current_width = 100

        def animate():
            menoo.place(relx=0.5, rely=0, relwidth=(menoo.current_width / 181.818), relheight=(menoo.current_width/250), anchor="n")
            menoo.current_width -= 0.1 + (40/menoo.current_width)
            if menoo.current_width > 0:
                self.root.after(5, animate)
            else:
                menoo.place_forget()

        ttk.Label(menoo, text="Test",style="Bw.TLabel").pack()
        Button(menoo, text="Press to Hide", command=animate,relief="flat",bg="#aaaaaa").pack(anchor="s", expand=1, fill="x", side="bottom", padx=1, pady=1,)

        
        menoo.place(relx=0.5, rely=0, relwidth=(menoo.current_width / 181.818), relheight=(menoo.current_width/250), anchor="n")

    def deprint(self,text):
        if self.settings["debug"]:
            print(text)

    def OpenFile(self):
        "Dialog for opening a file"
        filename = filedialog.askopenfilename(initialdir = '/',title = "Choose a file to edit",)
        if filename == "": return
        
        file_extension = os.path.splitext(filename)[1][1:]

        # Check if the file extension is associated with any tab
        for tabKind, extensions in self.settings["fileAssociations"].items():
            if file_extension in extensions:
                exec(f"{tabKind}(self,'{filename}')",{"tabs":tabs,"filename":filename,"self":self})
                return
        
        #Default to fileTab
        self.event_msg(1,"<<OpenFile>>")
        exec(f"tabs.FileTab(self,'{filename}')",{"tabs":tabs,"filename":filename,"self":self})
        
    def event_msg(self,code=0,sequence="<<None>>"):
        self.ext_mgr.event_msg(code) if not self.settings["experimentalExtensions"] else self.root.event_generate(sequence,when="now")

    def CreateFile(self):
        "Dialog for creating a new file"
        f = filedialog.asksaveasfile(mode='w')
        if f is None:
            return
        self.OpenFile(f.name)
        self.event_msg(2,"<<CreateFile>>")
    
    def DeleteFile(self):
        filename = filedialog.askopenfilename(initialdir = '/',title="Choose file to delete (Irreversible)",)
        os.remove(filename)
        self.event_msg(3,"<<DeleteFile>>")
    
    def RandomString(self):
        """Generates a random string, kind of like uuid, but not universally unique. Don't even ask why this exists."""
        return ''.join(random.choices(string.ascii_letters,k=10)) #1/(52^10) probability of being same.
    
    def PopupMenu(self,event:Event):
        def copy():
            event.widget.clipboard_clear()
            self.deprint(event.widget.selection_get())
            event.widget.clipboard_append(event.widget.selection_get())
        
        def cut():
            event.widget.clipboard_clear()
            self.deprint(event.widget.selection_get())
            delete()
            event.widget.clipboard_append(event.widget.selection_get())
        
        def paste():
            event.widget.insert("cursor",event.widget.clipboard_get())
        
        def delete():
            event.widget.delete("sel.first","sel.last")
        
        def google():
            from urllib.parse import quote
            from webbrowser import open as browseropen
            browseropen(f"https://www.google.com/?q={quote(event.widget.selection_get())}")
            del quote
            del browseropen
            #no need for this lol
   
            

        menu = Menu(self.root,tearoff=0)
        menu.add_command(label="Copy",command=lambda:copy())
        menu.add_command(label="Cut",command=lambda:cut())
        menu.add_command(label="Paste",command=lambda:paste())
        menu.add_command(label="Delete",command=lambda:delete())
        menu.add_command(label="Search selection",command=lambda:google())
        menu.add_separator()
        menu.post(event.x_root,event.y_root)



if __name__ == "__main__":
    Editor()
            
#*Build with
#*pyinstaller TkIDE.pyw -F -w -i icon.ico -n TkIDE  

#*Then use inno script installer to build the installer

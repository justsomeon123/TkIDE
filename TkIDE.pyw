#Version:1.5.5
#Look at README.md for more information
#############################################################################################
#TkIDE.pyw

import string,random,os,source.ImportantFunctions,json, source.SyntaxHighlighting,imghdr,contextlib,io#from extensions import * #import all extensions
from tkinter import ttk,filedialog,Text,Tk,StringVar,Menu,CURRENT,Toplevel,Button,BOTTOM,END,HORIZONTAL,DISABLED
from typing import Union
from source.CustomClasses import *
#Make sure pil is always after any modules with a class called Image or ImageTk
from PIL import Image, ImageTk


class Editor():
    def __init__(self) -> None:
        
        #SECTION:Setup
        self.root = Tk()

        with open('./assets/settings.json') as f:
            self.settings = json.load(f)
        with open(self.settings["EditorColors"]) as f:
            self.HighlightThemes:dict = json.load(f)

                
        self.FileName = StringVar()
        self.FileName.set('')
        self.FileContent = StringVar()

        self.MainIcon = PhotoImage('MainIcon',file=self.settings["icon"])
        self.FileIcon = PhotoImage('FileIcon',file=self.settings["file-icon"])
        self.root.bind('<Control-o>',lambda event:self.OpenFile())
        self.root.bind('<Control-s>',lambda event:self.Save())
        self.root.bind('<Control-n>',lambda event:self.CreateFile)
        self.root.bind('<Control-d>',lambda event:self.DeleteFileConfirm())
        self.root.bind('<Control-r>',lambda event:self.Run())


        

        #SECTION:Root Management        
        self.root.iconphoto(True,self.MainIcon)
        self.root.title('Tk IDE +')
        source.ImportantFunctions.FullScreen(self.root)

        #self.__settingsinit__()
        #SECTION:Menus  
        self.Menu = Menu(self.root)
        ##SUBSECTION:File Menu
        self.FileMenu = Menu(self.Menu,tearoff=0)
        self.FileMenu.add_command(label='Open File',command=lambda:self.OpenFile())
        self.FileMenu.add_command(label='Create a New File',command=lambda:self.CreateFile())
        self.FileMenu.add_command(label="Save",command=lambda:self.Save())
        self.FileMenu.add_separator(background="red")
        self.FileMenu.add_command(label="Delete a File",foreground="red",command=lambda:self.DeleteFileConfirm(),background="dark red")
        ##SUBSECTION:File Menu:END
        ##SUBSECTION:Run Menu
        self.RunMenu = Menu(self.Menu,tearoff=0)
        self.RunMenu.add_command(label='Run (PYTHON ONLY)',command=lambda:self.Run())
        #self.RunMenu.add_command(label='Run (PYTHON ONLY) with arguments',command=lambda:self.RunWithArgs())
        ##SUBSECTION:Run Menu:END
        ##SUBSECTION:Menu adding
        self.Menu.add_cascade(label="File",menu=self.FileMenu)
        self.Menu.add_cascade(label="Run",menu=self.RunMenu)
        self.root.config(menu=self.Menu)
        ##SUBSECTION:Menu adding:END
        
        #SECTION:Main Editor
        self.MainEditorCount = 0
        self.Pages = {}
        self.RandomTabStrings = []
        RandomString = self.RandomString()
        self.RandomTabStrings.append(RandomString)
        self.MainEditor = CustomNotebook(self.RandomTabStrings,self.Pages)
        self.MainEditor.pack(expand=True,fill=BOTH)
        E = self.Pages[RandomString]  = ttk.Frame(self.MainEditor)
        self.MainEditor.add(E, text=f"Home",image=self.MainIcon,compound="left")
        ttk.Label(E,text="Press this button or open the file via the menu at the top").pack(anchor=NW,pady=10)
        ttk.Button(E,text="Open File",command=lambda:self.OpenFile()).pack(anchor=NW)
        
        #SECTION:Loop
        self.root.mainloop()
        
    def Run(self):
        self.run_output = io.StringIO()

        index = self.MainEditor.index(CURRENT)
        RandomString = self.RandomTabStrings[index]
        Frame = self.Pages[RandomString]
        children = Frame.winfo_children()
        for child in children:
            if type(child) in [IDEText,Text]:
                self.Display = child
        with open(self.FileName.get(),'r') as f:
            resave = self.Display.get('1.0','end-1c')
            root = Toplevel()
            root.title(f'Run Output:{self.FileName.get()}')
            outputtext = Text(root,width=100,height=20)
            outputtext.pack(expand=True,fill=BOTH)
            with contextlib.redirect_stdout(self.run_output):
                exec(resave+"outputtext.insert(END,self.run_output.getvalue())")

    #SECTION:SAVE   
    def Save(self):
        index = self.MainEditor.index(CURRENT)
        RandomString = self.RandomTabStrings[index]
        Frame = self.Pages[RandomString]
        children = Frame.winfo_children()
        for child in children:
            if type(child) in [IDEText,Text]:
                self.Display = child
        with open(self.FileName.get(),'r+') as f:
            resave = self.Display.get('1.0','end-1c')
            f.truncate()
            f.write(resave)

    def OpenFile(self):
        filename = filedialog.askopenfilename(initialdir = '/',title = "Choose a file to edit",)
        if imghdr.what(filename) in ["png","gif","jpg","jpeg","ico"]:
            self.FileName.set(filename)
            self.ImageTab()
            return
        print(filename)
        self.FileName.set(filename)
        self.NewTab()

    def CreateFile(self):
        f = filedialog.asksaveasfile(mode='w')
        if f is None:
            return
        self.FileName.set(f.name)

    def DeleteFileConfirm(self):
        self.deleteroot = Toplevel()
        self.deleteroot.title('Are you sure?!')
        Label(self.deleteroot,text="Are you sure that you want to delete a file?").pack()
        Label(self.deleteroot,text="(Ireversible)",foreground="red").pack()
        self.DeleteButton = Button(self.deleteroot,text="Delete",foreground="red",activeforeground="dark red",background="dark red",activebackground="red",command=lambda:self.DeleteFile()).pack()
        self.CancelButton = Button(self.deleteroot,text="Cancel",command=lambda:self.deleteroot.destroy()).pack()
    
    def DeleteFile(self):
        filename = filedialog.askopenfilename(initialdir = '/',title    = "Choose file to delete",)
        os.remove(filename)
        self.deleteroot.destroy()
    
    def RandomString(self):
        return ''.join(random.choices(string.ascii_letters,k=10))

    def NewTab(self):
        with open(self.FileName.get(),encoding="UTF-8") as f:
            self.FileContent.set(f.read())
        
        self.MainEditorCount += 1
        RandomString = self.RandomString()
        self.RandomTabStrings.append(RandomString)
        E = self.Pages[RandomString]  = ttk.Frame(self.MainEditor)
        
        self.MainEditor.add(E, text=f"{self.FileName.get().split('/')[-1]}",image=self.FileIcon,compound="left")
        SVBar = Scrollbar(E)
        SVBar.pack (side = RIGHT, fill = "y")
        SHBar = Scrollbar(E, orient = HORIZONTAL)
        SHBar.pack (side = BOTTOM, fill = "x")
        Display = IDEText(E, height = 500, width = 500,yscrollcommand = SVBar.set,xscrollcommand = SHBar.set, wrap = "none")
        SaveButton = ttk.Button(E,text='Save',command=lambda:self.Save())
        SaveButton.pack(side=LEFT,fill=BOTH)
        Display.pack(expand = 0, fill = BOTH)
        SHBar.config(command = Display.xview)
        SVBar.config(command = Display.yview)
        quote = f"""{self.FileContent.get()}"""
        Display.insert(END, quote)
        #Higlighting
        self.ReHighlight(Display)
        self.root.bind("<KeyPress>",lambda event: self.ReHighlight(Display))
    
    def ImageTab(self):
        self.MainEditorCount += 1
        RandomString = self.RandomString()
        self.RandomTabStrings.append(RandomString)
        E = self.Pages[RandomString]  = ttk.Frame(self.MainEditor)

        self.MainEditor.add(E, text=f"{self.FileName.get().split('/')[-1]}",image=self.FileIcon,compound="left") 
        #n can't be zero
        n=self.settings['ImageSize']
        image = Image.open(self.FileName.get())
        print(image.size)
        print(f'({E.winfo_screenwidth()},{E.winfo_screenheight()})')
        if image.size[0] * n < E.winfo_screenwidth(): 
            print('got past step one')
            if image.size[1] * n < E.winfo_screenheight():        
                [imageSizeWidth, imageSizeHeight] = image.size
                newImageSizeWidth = int(imageSizeWidth*n)
                newImageSizeHeight = int(imageSizeHeight*n) 
                image = image.resize((newImageSizeWidth, newImageSizeHeight), Image.ANTIALIAS)
                print(image.size)
        img = ImageTk.PhotoImage(image)
        label = Label(E, image=img,text="testing")
        label.image = img # required for image to appear
        label.pack()

        

    def _findfiletype(self,file:str):
        e = file.split('.')
        c = e[-1]
        return c 
    

    
    def ReHighlight(self,Display:Union[IDEText,Text]):
        source.SyntaxHighlighting.PythonHighlight(Display,self.HighlightThemes)

    def ReadOnlyFile(self):
        self.Display.config(state=DISABLED)   
        
        
        


Editor()

#Build with

#pyinstaller --icon=icon.ico  --exclude-module _bootlocale   "TkIDE.pyw"
#Then use inno script installer to build the installer
#Version:1.5.5
#Look at README.md for more information
#############################################################################################
#TkIDE.pyw

import string,random,os,source.ImportantFunctions,json,imghdr
from extensions import * #import all extensions
from extensions import LoadExtensionPt
from tkinter import ttk,filedialog,Text,Tk,StringVar,Menu,Toplevel,Button,BOTTOM,END,HORIZONTAL,DISABLED,Entry,CURRENT
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
        self.root.bind('<Control-n>',lambda event:self.CreateFile())
        self.root.bind('<Control-d>',lambda event:self.DeleteFileConfirm())
        self.root.bind('<Control-r>',lambda event:self.Run())
        self.root.bind('<Control-Shift-p>',lambda event:self.ExtCommand())


        

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
        self.RunMenu.add_command(label='Run extension command',command=lambda:self.ExtCommand())
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
        self.Pages[RandomString]  = (ttk.Frame(self.MainEditor),self.FileName.get())
        E = self.Pages[RandomString][0]
        self.MainEditor.add(E, text=f"Home",image=self.root.MainIcon,compound="left")
        ttk.Label(E,text="Press this button or open the file via the menu at the top").pack(anchor=NW,pady=10)
        ttk.Button(E,text="Open File",command=lambda:self.OpenFile()).pack(anchor=NW)
        
        #SECTION:Loop
        self.root.mainloop()
    
    def OpenFolder(self):
        self.FolderName.set(filedialog.askdirectory(parent=self.root,title='Select a folder'))
        self.FolderTree.LoadNewFolder(self.FolderName.get())
    
    def Run(self):
        root = Toplevel()
        root.title('Run')
        text = Text(root)
        text.pack(expand=True,fill=BOTH)
        text.insert(END,"NOT IN USE:NO FUNCTIONALITY")
        text.configure(state=DISABLED)

    def ExtCommand(self):
        root = Toplevel()
        root.title('Run Command')
        command = StringVar()
        Entry(root,textvariable=command).pack(expand=True,fill=BOTH)
        Button(root,text='Run Provided Command',command=lambda:LoadExtensionPt(command.get().split("/"))).pack(side=BOTTOM)

    #SECTION:SAVE   
    def Save(self):
        index = self.MainEditor.index(CURRENT)
        RandomString = self.RandomTabStrings[index]
        Frame = self.Pages[RandomString][0]
        children = Frame.winfo_children()
        for child in children:
            if type(child) in [IDEText,Text]:
                self.Display = child
        with open(self.Pages[RandomString][1],'r+') as f:
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
        self.Pages[RandomString]  = (ttk.Frame(self.MainEditor),self.FileName.get())
        E = self.Pages[RandomString][0]
        self.MainEditor.add(E, text=f"{self.FileName.get().split('/')[-1]}",image=self.root.FileIcon,compound="left")
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
        PythonHighlight(Display,self.HighlightThemes)
        self.root.bind("<KeyPress>",lambda event: PythonHighlight(Display,self.HighlightThemes))
    
    def ImageTab(self):
        self.MainEditorCount += 1
        RandomString = self.RandomString()
        self.RandomTabStrings.append(RandomString)
        self.Pages[RandomString]  = (ttk.Frame(self.MainEditor),self.FileName.get())
        E = self.Pages[RandomString][0]

        self.MainEditor.add(E, text=f"Tab {self.FileName.get()}",image=self.FileIcon,compound="left") 
        #n can't be zero
        n=8
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
    
        
        
        


Editor()

#Build with

#pyinstaller --icon=icon.ico  --exclude-module "_bootlocale "  "TkIDE.pyw"
#Then use inno script installer to build the installer
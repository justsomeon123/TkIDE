#INFO Version:2.0 Last Updated:2022-07-5
#Look at README.md for more information
#############################################################################################
#TkIDE.pyw

import string,random,os,source.ImportantFunctions,json,imghdr
from tkinter import ttk,filedialog,Text,Tk,StringVar,Menu,Toplevel,Button,BOTTOM,END,HORIZONTAL,Entry,CURRENT
from source.CustomClasses import *
#Make sure pil is always after any modules with a class called Image or ImageTk
from PIL import Image, ImageTk

def deprint(text,debug=False):
    if debug:
        print(text)
        
class Editor:
    def __init__(self) -> None:
        #SECTION:Setup
        self.root = Tk()

        with open('./assets/settings.json') as f:
            self.settings = json.load(f)

                
        self.FileName = StringVar()
        self.FileName.set('')
        self.FileContent = StringVar()

        #SECTION:Icons
        self.root.MainIcon = ImageTk.PhotoImage(Image.open(self.settings["icon"]),Image.NEAREST)
        self.root.FileIcon = ImageTk.PhotoImage(Image.open(self.settings["file-icon"]),Image.NEAREST)

        #SECTION:Shortcuts
        self.root.bind('<Control-o>',lambda event:self.OpenFile())
        self.root.bind('<Control-s>',lambda event:self.Save())
        self.root.bind('<Control-n>',lambda event:self.CreateFile())
        self.root.bind('<Control-d>',lambda event:self.DeleteFileConfirm())
        self.root.bind('<Control-r>',lambda event:self.Run())


        

        #SECTION:Root Management        
        self.root.iconphoto(True,self.root.MainIcon)    
        self.root.title('TkIDE')
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
        ttk.Label(E,text="Press these buttons or use the menu at the top").pack(anchor=NW,pady=10)
        ttk.Button(E,text="Open File",command=lambda:self.OpenFile()).pack(anchor=NW)
        ttk.Button(E,text="Create a New File",command=lambda:self.CreateFile()).pack(anchor=NW)
        ttk.Button(E,text="Delete a File",command=lambda:self.DeleteFileConfirm()).pack(anchor=NW)
        
        
        #SECTION:Loop
        self.root.mainloop()
    
    
    def Run(self):
        root = Toplevel()
        root.title('Run')
        text = Text(root)
        text.pack(expand=True,fill=BOTH)
        text.insert(END,"NOT USED:NO FUNCTIONALITY YET")    


    def ExtCommand(self):
        root = Toplevel()
        root.title('Run Command')
        command = StringVar()
        Entry(root,textvariable=command).pack(expand=True,fill=BOTH)
        Button(root,text='Run Provided Command',command=lambda:self.iel(root,command.get().split("/"))).pack(side=BOTTOM)


    #SECTION:SAVE   
    def Save(self):
        index = self.MainEditor.index(CURRENT)
        RandomString = self.RandomTabStrings[index]
        Frame = self.Pages[RandomString][0]
        children = Frame.winfo_children()

        for child in children:
            if type(child) == IDEText:
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
        deprint(filename)
        self.FileName.set(filename)
        self.NewTab()

    def CreateFile(self):
        f = filedialog.asksaveasfile(mode='w')
        if f is None:
            return
        self.FileName.set(f.name)
        self.NewTab()

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
    
    def PopupMenu(self,event):
        def Copy():
            event.widget.clipboard_clear()
            deprint(event.widget.selection_get())
            event.widget.clipboard_append(event.widget.selection_get())
        menu = Menu(self.root,tearoff=0)
        menu.add_command(label="Copy",command=lambda:Copy())
        menu.add_command(label="Warning!:Might not work")
        menu.post(event.x_root,event.y_root)

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
        deprint(self.FileName.get(),True)
        Display = IDEText(E,filename=self.FileName.get(),height = 500, width = 500,yscrollcommand = SVBar.set,xscrollcommand = SHBar.set, wrap = "none")
        Display.pack(expand = 0, fill = BOTH)
        Display.bind("<Button-3>",lambda event:self.PopupMenu(event))
        SHBar.config(command = Display.xview)
        SVBar.config(command = Display.yview)
        Display.insert(END,  f"""{self.FileContent.get()}""")
        
        #@ Higlighting Code
        source.ImportantFunctions.highlight(Display)
        self.root.bind("<KeyPress>",lambda event: source.ImportantFunctions.highlight(Display))
    
    def ImageTab(self):
        self.MainEditorCount += 1
        RandomString = self.RandomString()
        self.RandomTabStrings.append(RandomString)
        self.Pages[RandomString]  = (ttk.Frame(self.MainEditor),self.FileName.get())
        E = self.Pages[RandomString][0]
        self.MainEditor.add(E, text=f"{self.FileName.get().split('/')[-1]}",image=self.root.FileIcon,compound="left") 
        #@ ^  creating a tab for the image holder.

        #WARN size can't be zero
        
        #@ v resize the image until it fits inside without being too big.
        size=self.settings['ImageScaleSize']
        image = Image.open(self.FileName.get())
        if image.size[0] * size < E.winfo_screenwidth(): 
            if image.size[1] * size < E.winfo_screenheight():        
                [imageSizeWidth, imageSizeHeight] = image.size
                newImageSizeWidth = int(imageSizeWidth*size)
                newImageSizeHeight = int(imageSizeHeight*size) 
                image = image.resize((newImageSizeWidth, newImageSizeHeight), Image.NEAREST)



        #! v NOT WORKING CODE FOR GIFS
        ''' 
        for frame in range(0,image.n_frames):
            image.seek(frame)
            n=self.settings['ImageSize']
            image = image
            deprint(image.size) 
            deprint(f'({E.winfo_screenwidth()},{E.winfo_screenheight()})')
            if image.size[0] * n < E.winfo_screenwidth(): 
                deprint('got past step one')
                if image.size[1] * n < E.winfo_screenheight():        
                    [imageSizeWidth, imageSizeHeight] = image.size
                    newImageSizeWidth = int(imageSizeWidth*n)
                    newImageSizeHeight = int(imageSizeHeight*n) 
                    image = image.resize((newImageSizeWidth, newImageSizeHeight), Image.ANTIALIAS)
        '''
    
        #@ Handles packing and showing the image in the screen.
        img = ImageTk.PhotoImage(image)
        label = Label(E, image=img,text="Image not supported/not Loaded")
        label.image = img #WARN required for image to appear
        label.pack()

        
    


if __name__ == "__main__":
    Editor()
            
#*Build with
#*pyinstaller TkIDE.pyw -F -w -i icon.ico -n TkIDE  

#*Then use inno script installer to create the installer

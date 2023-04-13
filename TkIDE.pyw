#INFO Version:2.1 Last Updated:2023-02-23
#Look at README.md for more information
#############################################################################################
#TkIDE.pyw

import string,random,os,source.ImportantFunctions,json
from tkinter import Event, ttk,filedialog,Tk,StringVar,Menu,Toplevel,Button,BOTTOM,END,HORIZONTAL,CURRENT,NW,RIGHT,BOTH,Scrollbar,Label
import source.CustomClasses as cc
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

                

        #SECTION:Icons
        self.root.MainIcon = ImageTk.PhotoImage(Image.open(self.settings["icon"]),Image.Resampling.NEAREST)
        self.root.FileIcon = ImageTk.PhotoImage(Image.open(self.settings["file-icon"]),Image.Resampling.NEAREST)
        self.root.ImageIcon = ImageTk.PhotoImage(Image.open(self.settings["image-icon"]),Image.Resampling.NEAREST)

        #SECTION:Shortcuts
        self.root.bind('<Control-o>',lambda event:self.OpenFile())
        self.root.bind('<Control-s>',lambda event:self.Save())
        self.root.bind('<Control-n>',lambda event:self.CreateFile())
        self.root.bind('<Control-d>',lambda event:self.DeleteFileConfirm())
        self.root.bind('<Control-`>',lambda event:self.Terminal())


        

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

        ##SUBSECTION:Terminal Menu
        self.TerminalMenu = Menu(self.Menu,tearoff=0)
        self.TerminalMenu.add_command(label='Terminal',command=lambda:self.Terminal())
        ##SUBSECTION:Terminal Menu:END

        ##SUBSECTION:Menu adding
        self.Menu.add_cascade(label="File",menu=self.FileMenu)
        self.Menu.add_cascade(label="Terminal",menu=self.TerminalMenu)
        self.root.config(menu=self.Menu)
        ##SUBSECTION:Menu adding:END
        
        #SECTION:Main Editor
        self.MainEditorCount = 0 #Tab count.
        self.Pages = {} #dictionary of pages/tabs and their key values
        self.RandomTabStrings = [] #Random strings that correspond to each page , look at self.RandomString() for more info.
        self.MainEditor = cc.CustomNotebook(self.RandomTabStrings,self.Pages) #the main editor interface. (View CustomClasses.CustomNotebook for more information)
        self.MainEditor.pack(expand=True,fill=BOTH)




        ##SECTION:Welcome Page
        tab_identifier = self.RandomString() #Creates a tab identifier for this tab.
        self.RandomTabStrings.append(tab_identifier) #Adds it to the storage of tab identifiers.
        self.Pages[tab_identifier]  = (ttk.Frame(self.MainEditor),"welcomepage") #Stores the informaton on each pages critical parts
        E = self.Pages[tab_identifier][0] #E is the Frame holding the editor/page content
        self.MainEditor.add(E, text=f"Home",image=self.root.MainIcon,compound="left") # Add a tab.
        ttk.Label(E,text="Press these buttons or use the menu at the top").pack(anchor=NW,pady=10) #Buttons on welcome page.
        ttk.Button(E,text="Open File",command=lambda:self.OpenFile()).pack(anchor=NW)
        ttk.Button(E,text="Create a New File",command=lambda:self.CreateFile()).pack(anchor=NW)
        ttk.Button(E,text="Delete a File",command=lambda:self.DeleteFileConfirm()).pack(anchor=NW)
        
        
        #SECTION:Loop
        self.root.mainloop() #Gui loop.
    
    
    def Terminal(self):
        cc.TerminalWindow(self)


    #SECTION:SAVE   
    def Save(self):
        "Quick code to save current editor (text) state to the file."
        index = self.MainEditor.index(CURRENT)
        tab_identifier = self.RandomTabStrings[index]
        Frame = self.Pages[tab_identifier][0]
        children = Frame.winfo_children()

        for child in children:
            if type(child) == cc.IDEText:
                self.Display = child

        with open(self.Pages[tab_identifier][1],'r+') as f:
            resave = self.Display.get('1.0','end-1c')
            f.truncate()
            f.write(resave)

    def OpenFile(self):
        "Dialog for opening a file"
        filename = filedialog.askopenfilename(initialdir = '/',title = "Choose a file to edit",)
        if filename.endswith(("png","gif","jpg","jpeg","ico")):
            self.ImageTab(filename)
            return
        deprint(filename)
        self.NewTab(filename)

    def CreateFile(self):
        "Dialog for creating a new file"
        f = filedialog.asksaveasfile(mode='w')
        if f is None:
            return
        self.NewTab(f.name)

    def DeleteFileConfirm(self):
        """The confirmation dialog for deleting a file"""
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
        """Generates a random string, kind of like uuid, but not universally unique. Don't even ask why this exists."""
        return ''.join(random.choices(string.ascii_letters,k=10)) #1/141167095653376 chance to be the same (at least i think so.)
    
    def PopupMenu(self,event:Event):
        def Copy():
            event.widget.clipboard_clear()
            deprint(event.widget.selection_get())
            event.widget.clipboard_append(event.widget.selection_get())
        
        def Cut():
            event.widget.clipboard_clear()
            deprint(event.widget.selection_get())
            event.widget.delete("sel.first","sel.last")
            event.widget.clipboard_append(event.widget.selection_get())
        
        def Paste():
            event.widget.insert("sel.first",event.widget.clipboard_get())
        
        def Delete():
            event.widget.delete("sel.first","sel.last")
            

        menu = Menu(self.root,tearoff=0)
        menu.add_command(label="Copy",command=lambda:Copy())
        menu.add_command(label="Cut",command=lambda:Cut())
        menu.add_command(label="Paste",command=lambda:Paste())
        menu.add_command(label="Delete",command=lambda:Delete())
        menu.add_separator()
        menu.add_command(label="Warning: Might not work.",background="#dd2222")
        menu.post(event.x_root,event.y_root)

    def NewTab(self,filename):
        with open(filename,encoding="UTF-8") as f:
            filecontent= f.read()
        
        #@ I don't even know. This code is unreadable. Please send help.
        self.MainEditorCount += 1
        tab_identifier = self.RandomString()
        self.RandomTabStrings.append(tab_identifier)
        self.Pages[tab_identifier]  = (ttk.Frame(self.MainEditor),filename)
        E = self.Pages[tab_identifier][0]        


        self.MainEditor.add(E, text=f"{filename.split('/')[-1]}",image=self.root.FileIcon,compound="left")



        SVBar = Scrollbar(E)
        SVBar.pack (side = RIGHT, fill = "y")
        SHBar = Scrollbar(E, orient = HORIZONTAL)
        SHBar.pack (side = BOTTOM, fill = "x")

        deprint(filename,True)

        Display = cc.IDEText(E,filename=filename,height = 500, width = 500,yscrollcommand = SVBar.set,xscrollcommand = SHBar.set, wrap = "none")
        Display.pack(expand = 0, fill = BOTH)
        Display.bind("<Button-3>",lambda event:self.PopupMenu(event))


        SHBar.config(command = Display.xview)
        SVBar.config(command = Display.yview)

        Display.insert(END,  f"""{filecontent}""")
        


        #@ Higlighting Code
        source.ImportantFunctions.highlight(Display)
        self.root.bind("<KeyRelease>",lambda event: source.ImportantFunctions.highlight(Display))



    def ImageTab(self,filename):
        self.MainEditorCount += 1
        tab_identifier = self.RandomString()
        self.RandomTabStrings.append(tab_identifier)
        self.Pages[tab_identifier]  = (ttk.Frame(self.MainEditor),filename)
        E = self.Pages[tab_identifier][0]
        self.MainEditor.add(E, text=f"{filename.split('/')[-1]}",image=self.root.ImageIcon,compound="left") 
        #@ ^  creating a tab for the image holder.

        #WARN size can't be zero
        
        #@ v resize the image until it fits inside without being too big.
        size=self.settings['ImageScaleSize']
        image = Image.open(filename)
        if image.size[0] * size < E.winfo_screenwidth(): 
            if image.size[1] * size < E.winfo_screenheight():        
                [imageSizeWidth, imageSizeHeight] = image.size
                newImageSizeWidth = int(imageSizeWidth*size)
                newImageSizeHeight = int(imageSizeHeight*size) 
                image = image.resize((newImageSizeWidth, newImageSizeHeight), Image.Resampling.NEAREST)



        #! v BROKEN CODE FOR GIFS
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
        label = Label(E, image=img,text="Image not supported/cannot be loaded")
        label.image = img #WARN required for image to appear
        label.pack()

        
    


if __name__ == "__main__":
    Editor()
            
#*Build with
#*pyinstaller TkIDE.pyw -F -w -i icon.ico -n TkIDE  

#*Then use inno script installer to build the installer

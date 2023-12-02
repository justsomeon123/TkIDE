from tkinter import (ttk,BOTTOM,RIGHT,Scrollbar,HORIZONTAL,BOTH,END,Label)
from . import CustomClasses as cc

from PIL import Image,ImageTk

#Created in an attempt to de-legacy this code.
#Go-to origin.md for more info.

class Tab():
    def __init__(self,master,title,**kwargs) -> None:
        master.TabCount += 1
        tab_identifier = master.RandomString()
        master.TabIdentifiers.append(tab_identifier)
        master.Pages[tab_identifier]  = (ttk.Frame(master.EditorPages),title)
        self.PageFrame = master.Pages[tab_identifier][0]        
        
        master.EditorPages.add(self.PageFrame, text=title,image=kwargs["icon"],compound="left")

class FileTab(Tab):
    def __init__(self,master,filename):
        #you can tell i suck lmao
        super(FileTab,self).__init__(master,filename,icon=master.root.FileIcon)

        with open(filename,encoding="UTF-8") as f:
            filecontent= f.read()  
    
        SVBar = Scrollbar(self.PageFrame)
        SVBar.pack(side = RIGHT, fill = "y")
        SHBar = Scrollbar(self.PageFrame, orient = HORIZONTAL)
        SHBar.pack(side = BOTTOM, fill = "x")

        master.deprint(filename)

        Display = cc.IDEText(self.PageFrame,filename=filename,height = 500, width = 500,yscrollcommand = SVBar.set,xscrollcommand = SHBar.set, wrap = "none")
        Display.pack(expand = 0, fill = BOTH)
        Display.bind("<Button-3>",lambda event:master.PopupMenu(event))


        SHBar.config(command = Display.xview)
        SVBar.config(command = Display.yview)

        Display.insert(END,  f"""{filecontent}""")
        


        #@ Higlighting Code
        if master.settings["enableHighlighting"]:
            Display.highlight()
            master.root.bind("<KeyRelease>",lambda event: Display.highlight())

class ImageTab(Tab):
    def __init__(self,master,filename):
        super(ImageTab, self).__init__(master,filename,icon=master.root.ImageIcon)
        
        #@ v resize the image until it fits inside without being too big.
        size= master.settings['imageResizeCoeffiecent']
        image = Image.open(filename)
        if image.size[0] * size < self.PageFrame.winfo_screenwidth(): 
            if image.size[1] * size < self.PageFrame.winfo_screenheight():        
                [imageSizeWidth, imageSizeHeight] = image.size
                newImageSizeWidth = int(imageSizeWidth*size)
                newImageSizeHeight = int(imageSizeHeight*size) 
                image = image.resize((newImageSizeWidth, newImageSizeHeight), Image.Resampling.NEAREST)

        #@ Handles packing and showing the image in the screen.
        img = ImageTk.PhotoImage(image)
        label = Label(self.PageFrame, image=img,text="Image not supported/cannot be loaded")
        label.image = img #WARN required for image to appear
        label.pack()
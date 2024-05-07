"""Modularizes tabs into a different section of code. More expandable."""

from tkinter import (BOTH, BOTTOM, END, HORIZONTAL, RIGHT, Frame, Label,
                     Scrollbar, ttk)

from PIL import Image, ImageTk

import source.CustomClasses as cc

#Created in an attempt to de-legacy this code.
#Go-to origin.md for more info.

class Tab():
    def __init__(self,master,title,icon="",**kwargs) -> None:
        master.TabCount += 1
        tab_identifier = master.RandomString()
        master.TabIdentifiers.append(tab_identifier)
        master.Pages[tab_identifier]  = (ttk.Frame(master.EditorPages),title)
        self.PageFrame:Frame = master.Pages[tab_identifier][0]
        if icon == "": icon = master.FileIcon

        master.EditorPages.add(self.PageFrame, text=title,image=icon,compound="left")

class FileTab(Tab):
    def __init__(self,master,filename):
        
        super(FileTab,self).__init__(master,filename,icon=master.FileIcon)

        with open(filename,encoding="UTF-8") as f:
            filecontent= f.read()  
    
        SVBar = Scrollbar(self.PageFrame)
        SVBar.pack(side = RIGHT, fill = "y")
        SHBar = Scrollbar(self.PageFrame, orient = HORIZONTAL)
        SHBar.pack(side = BOTTOM, fill = "x")

        master.deprint(filename)

        self.TextBox = cc.IDEText(self.PageFrame,filename=filename,height = 500, width = 500,yscrollcommand = SVBar.set,xscrollcommand = SHBar.set, wrap = "none")
        self.TextBox.pack(expand = 0, fill = BOTH)
        self.TextBox.bind("<Button-3>",lambda event:master.PopupMenu(event))


        SHBar.config(command = self.TextBox.xview)
        SVBar.config(command = self.TextBox.yview)

        self.TextBox.insert(END,  f"""{filecontent}""")


        #@ Higlighting Code
        if master.settings["enableHighlighting"]:
            self.TextBox.highlight()
            self.TextBox.bind("<KeyRelease>",lambda event: self.TextBox.highlight())
        
    def Save(self):
        "Quick code to save current editor (text) state to the file."
        with open(self.TextBox.filename,'r+') as f:
            resave = self.TextBox.get('1.0','end-1c')
            f.truncate()
            f.write(resave)

class ImageTab(Tab):
    def __init__(self,master,filename):
        super(ImageTab, self).__init__(master,filename,icon=master.ImageIcon)
        
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
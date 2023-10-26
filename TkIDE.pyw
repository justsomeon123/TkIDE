#INFO Version:2.2.1 Last Updated:2023-09-1
#Look at README.md for more information
#############################################################################################
#TkIDE.pyw


import json
import os
import random
import socket
import string
import threading  # Extension communication.
from tkinter import (BOTH, BOTTOM, CURRENT, END, HORIZONTAL, NW, RIGHT, Button,
                     Event, Label, Menu, Scrollbar, Tk, Toplevel, filedialog,
                     messagebox, ttk)

#Make sure pil is always imported after any modules with a class called Image or ImageTk
from PIL import Image, ImageTk

import source.CustomClasses as cc
import source.term as Terminal
import source.ImportantFunctions


class Editor:
    def __init__(self) -> None:
        #SECTION:Setup
        self.root = Tk()
        

        with open('./assets/settings.json') as f:
            self.settings = json.load(f)
        

        self.ext_server_init(settings=self.settings)
            

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
        self.EditorPages.add(PageFrame, text=f"Home",image=self.root.MainIcon,compound="left") # Add a tab.
        ttk.Label(PageFrame,text="Press these buttons or use the menu at the top").pack(anchor=NW,pady=10) #Buttons on welcome page.
        ttk.Button(PageFrame,text="Open File",command=lambda:self.OpenFile()).pack(anchor=NW)
        ttk.Button(PageFrame,text="Create a New File",command=lambda:self.CreateFile()).pack(anchor=NW)
        ttk.Button(PageFrame,text="Delete a File",command=lambda:self.DeleteFileConfirm()).pack(anchor=NW)
        
        if not self.settings["enableHighlighting"]:
            messagebox.showinfo("Highlighting","Highlighting is disabled. Go to settings to enable it.")

        #SECTION:Loop
        self.root.mainloop() #Gui loop.

    def deprint(self,text):
        if self.settings["debug"]:
            print(text)
    
    def ext_server_init(self,settings):
        self.extension_connections = {}
        self.server_thread = threading.Thread(target=self.ext_server,args=())
        self.server_thread.daemon = True #background thread
        if settings["extensionsEnabled"]:
            self.server_thread.start()

    def ext_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ("localhost",49155) #port in dynamic range.
        server_socket.bind(server_address)
        server_socket.listen(self.settings["maxExtConnections"]*2) #Double it so that each extension can listen to events.
        self.deprint("server listening")
        while True:
            client_socket, client_address = server_socket.accept() #Client socket is the socket created by the server to communicate with the client.
            self.deprint(f"client connect:{client_address}")

            #Starts a thread to handle the client called client thread
            client_thread = threading.Thread(target=self.client_handle,args=(client_socket,))
            client_thread.daemon = True
            client_thread.start()
    
    def event_msg(self, code):
        #connection_key is the uid for each connection. self.extension_connections[connection_key] -> [""]
        for connection_key in self.extension_connections: 
            try:
                self.extension_connections[connection_key][1].send(f"SE:{code}".encode())
            except ConnectionAbortedError:
                self.extension_connections.pop(self.extension_connections[connection_key])
        
    def client_handle(self,client_socket:socket.socket):
        #INFO Client socket is actually a subsocket created by the server to respond to the actual request
        #INFO (cont.) /communicate with the real client.

        sockclose = False
        while not sockclose:
            data = client_socket.recv(1024).decode() #Recieve data.

            #Initial info.
            if not data.startswith("ER:") and not data.startswith("ELR:"):
                data = int(data)


            elif (type(data)!=int) and (data.startswith('ER:')): #Connection accepted.
                idn = self.RandomString()
                client_socket.send(f"{idn}".encode())
                self.extension_connections[idn] = [data.removeprefix('ER:'),client_socket]
            
            elif (type(data)!=int) and (data.startswith('ELR:')):
                idn = data.removeprefix("ELR:") #Event Listener for extension with code idn.
                self.extension_connections[idn].append(client_socket)
            
            elif data == 0:
                sockclose = True
                client_socket.close()

            #INFO READ FUNCTIONS BELOW. READ FUNCTIONS START WITH 1.   

            elif data == 11:
                #This code is adapted from the save function below
                display = 0
                for child in self.Pages[self.TabIdentifiers[self.EditorPages.index(CURRENT)]][0].winfo_children():
                    if (display == 0): #I feel like this code is demented. I wrote it at 4 am idrk.
                        display = 0
                    if type(child) == cc.IDEText:
                        display = child
                if display == 0:
                    client_socket.send("NO-TEXT".encode())
                else:
                    client_socket.send(display.get("0.0",END).encode())

            elif data == 12:
                #Turns out this also works to get the filename.
                display = 0
                for child in self.Pages[self.TabIdentifiers[self.EditorPages.index(CURRENT)]][0].winfo_children():
                    if (display == 0): #I feel like this code is demented. I wrote it at 4 am idrk.
                        display = 0
                    if type(child) == cc.IDEText:
                        display = child
                if display == 0:
                    client_socket.send("NO-FILE".encode())
                else:
                    client_socket.send(display.filename.encode())
            
            elif data == 13:
                client_socket.send(str(len(self.EditorPages.tabs())).encode())

            #INFO UNKNOWN CODES
            else:
                client_socket.send("CODE-INVALID".encode())
            
            
    
    
    def Terminal(self):
        Terminal.TerminalWindow(self)


    #SECTION:SAVE   
    def Save(self):
        "Quick code to save current editor (text) state to the file."
        index = self.EditorPages.index(CURRENT)
        tab_identifier = self.TabIdentifiers[index]
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
        self.deprint(filename)
        self.NewTab(filename)
        self.event_msg(1)

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
        Button(self.deleteroot,text="Delete",foreground="red",activeforeground="dark red",background="dark red",activebackground="red",command=lambda:self.DeleteFile()).pack()
        Button(self.deleteroot,text="Cancel",command=lambda:self.deleteroot.destroy()).pack()
    
    def DeleteFile(self):
        filename = filedialog.askopenfilename(initialdir = '/',title    = "Choose file to delete",)
        os.remove(filename)
        self.deleteroot.destroy()
    
    def RandomString(self):
        """Generates a random string, kind of like uuid, but not universally unique. Don't even ask why this exists."""
        return ''.join(random.choices(string.ascii_letters,k=10)) #1/141167095653376 chance to be the same (at least i think so.)
    
    def PopupMenu(self,event:Event):
        def copy():
            event.widget.clipboard_clear()
            self.deprint(event.widget.selection_get())
            event.widget.clipboard_append(event.widget.selection_get())
        
        def cut():
            event.widget.clipboard_clear()
            self.deprint(event.widget.selection_get())
            event.widget.delete("sel.first","sel.last")
            event.widget.clipboard_append(event.widget.selection_get())
        
        def paste():
            event.widget.insert("sel.first",event.widget.clipboard_get())
        
        def delete():
            event.widget.delete("sel.first","sel.last")
        
        def google():
            from urllib.parse import quote
            from webbrowser import open as browseropen
            browseropen(f"https://www.google.com/?q={quote(event.widget.selection_get())}")
            del quote
            del browseropen
            #always be secure kids!
   
            

        menu = Menu(self.root,tearoff=0)
        menu.add_command(label="Copy",command=lambda:copy())
        menu.add_command(label="Cut",command=lambda:cut())
        menu.add_command(label="Paste",command=lambda:paste())
        menu.add_command(label="Delete",command=lambda:delete())
        menu.add_command(label="Search selection",command=lambda:google())
        menu.add_separator()
        menu.post(event.x_root,event.y_root)

    def NewTab(self,filename):
        with open(filename,encoding="UTF-8") as f:
            filecontent= f.read()
        
        #@ I don't even know. This code is unreadable. Please send help.
        self.TabCount += 1
        tab_identifier = self.RandomString()
        self.TabIdentifiers.append(tab_identifier)
        self.Pages[tab_identifier]  = (ttk.Frame(self.EditorPages),filename)
        PageFrame = self.Pages[tab_identifier][0]        


        self.EditorPages.add(PageFrame, text=f"{filename.split('/')[-1]}",image=self.root.FileIcon,compound="left")



        SVBar = Scrollbar(PageFrame)
        SVBar.pack(side = RIGHT, fill = "y")
        SHBar = Scrollbar(PageFrame, orient = HORIZONTAL)
        SHBar.pack(side = BOTTOM, fill = "x")

        self.deprint(filename)

        Display = cc.IDEText(PageFrame,filename=filename,height = 500, width = 500,yscrollcommand = SVBar.set,xscrollcommand = SHBar.set, wrap = "none")
        Display.pack(expand = 0, fill = BOTH)
        Display.bind("<Button-3>",lambda event:self.PopupMenu(event))


        SHBar.config(command = Display.xview)
        SVBar.config(command = Display.yview)

        Display.insert(END,  f"""{filecontent}""")
        


        #@ Higlighting Code
        if self.settings["enableHighlighting"]:
            source.ImportantFunctions.highlight(Display)
            self.root.bind("<KeyRelease>",lambda event: source.ImportantFunctions.highlight(Display))

            



    def ImageTab(self,filename):
        self.TabCount += 1
        tab_identifier = self.RandomString()
        self.TabIdentifiers.append(tab_identifier)
        self.Pages[tab_identifier]  = (ttk.Frame(self.EditorPages),filename)
        PageFrame = self.Pages[tab_identifier][0]
        self.EditorPages.add(PageFrame, text=f"{filename.split('/')[-1]}",image=self.root.ImageIcon,compound="left") 
        #@ ^  creating a tab for the image holder.

        #WARN size can't be zero
        
        #@ v resize the image until it fits inside without being too big.
        size=self.settings['imageResizeCoeffiecent']
        image = Image.open(filename)
        if image.size[0] * size < PageFrame.winfo_screenwidth(): 
            if image.size[1] * size < PageFrame.winfo_screenheight():        
                [imageSizeWidth, imageSizeHeight] = image.size
                newImageSizeWidth = int(imageSizeWidth*size)
                newImageSizeHeight = int(imageSizeHeight*size) 
                image = image.resize((newImageSizeWidth, newImageSizeHeight), Image.Resampling.NEAREST)
    
        #@ Handles packing and showing the image in the screen.
        img = ImageTk.PhotoImage(image)
        label = Label(PageFrame, image=img,text="Image not supported/cannot be loaded")
        label.image = img #WARN required for image to appear
        label.pack()

        
    


if __name__ == "__main__":
    Editor()
            
#*Build with
#*pyinstaller TkIDE.pyw -F -w -i icon.ico -n TkIDE  

#*Then use inno script installer to build the installer

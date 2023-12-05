#Version:2.6 Last Updated:2023-12-1
#Look at README.md for more information
#############################################################################################
#TkIDE.pyw


import json
import os
import random
import socket
import string
import threading
from tkinter import (BOTH, CURRENT, END, NW, Event, Menu, Tk, filedialog,
                     messagebox, ttk)

#Make sure pil is always imported after any modules with a class called Image or ImageTk
from PIL import Image, ImageTk

#Internal imports
import source.CustomClasses as cc
import source.ImportantFunctions
import source.tabs as tabs
import source.term as Terminal


class Editor:
    def __init__(self) -> None:
        #SECTION:Setup
        self.root = Tk()
        

        with open('./assets/settings.json') as f:
            self.settings = json.load(f)
        

        self.ext_server_init(settings=self.settings)
            

        #SECTION:Icons 
        MainIcon = ImageTk.PhotoImage(Image.open(self.settings["icon"]),Image.Resampling.NEAREST)
        self.FileIcon = ImageTk.PhotoImage(Image.open(self.settings["file-icon"]),Image.Resampling.NEAREST)
        self.ImageIcon = ImageTk.PhotoImage(Image.open(self.settings["image-icon"]),Image.Resampling.NEAREST)

        #SECTION:Shortcuts
        self.root.bind('<Control-o>',lambda event:self.OpenFile())
        self.root.bind('<Control-n>',lambda event:self.CreateFile())
        self.root.bind('<Control-`>',lambda event:self.Terminal())

        #SECTION:Root Management        
        self.root.iconphoto(True,MainIcon)     
        self.root.title('TkIDE')
        source.ImportantFunctions.FullScreen(self.root)

        #self.__settingsinit__()
        #SECTION:Menus  
        self.Menu = Menu(self.root)
        ##SUBSECTION:File Menu
        FileMenu = Menu(self.Menu,tearoff=0)
        FileMenu.add_command(label='Open File',command=lambda:self.OpenFile())
        FileMenu.add_command(label='Create a New File',command=lambda:self.CreateFile())
        FileMenu.add_command(label="Save",command=lambda:self.Save())
        FileMenu.add_separator(background="red")
        FileMenu.add_command(label="Delete a File",foreground="red",command=lambda:self.DeleteFileConfirm(),background="dark red")
        ##SUBSECTION:File Menu:END

        ##SUBSECTION:Terminal Menu
        TerminalMenu = Menu(self.Menu,tearoff=0)
        TerminalMenu.add_command(label='Terminal',command=lambda:Terminal.TerminalWindow(self))
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
            if self.settings["experimentalExtensions"]:
                client_thread = threading.Thread(target=self.client_handle,args=(client_socket,))
            else:
                client_thread = threading.Thread(target=self.old_client_handle,args=(client_socket,))
            client_thread.daemon = True
            client_thread.start()
    
    def event_msg(self, code):
        #connection_key is the uid for each connection. self.extension_connections[connection_key] -> [""]
        for connection_key in self.extension_connections.copy(): 
            try:
                self.extension_connections[connection_key][2].send(f"SE:{code}".encode())
            except ConnectionResetError:
                print(self.extension_connections[connection_key])
                self.extension_connections.pop(connection_key)
                continue
    
    def old_client_handle(self,client_socket:socket.socket):
        #NOTE: Old code that doesn't support events, but also works completely as expected.

        #INFO Client socket is actually a subsocket created by the server to respond to the actual request
        #INFO (cont.) /communicate with the real client.

        sockclose = False
        while not sockclose:
            data = client_socket.recv(1024).decode() #Recieve data.

            #Initial info.
            if not data.startswith("ER:"):
                data = int(data)


            if (type(data)!=int) and (data.startswith('ER:')): #Connection accepted.
                idn = self.RandomString()
                client_socket.send(f"{idn}".encode())
                self.extension_connections[idn] = data.removeprefix('ER:')
            
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

    def OpenFile(self):
        "Dialog for opening a file"
        filename = filedialog.askopenfilename(initialdir = '/',title = "Choose a file to edit",)
        file_extension = os.path.splitext(filename)[1][1:]

        # Check if the file extension is associated with any tab
        for tab, extensions in self.settings["fileAssociations"].items():
            if file_extension in extensions:
                exec(f"{tab}(self,'{filename}')",{"tabs":tabs,"filename":filename,"self":self})
                return
        
        exec(f"tabs.FileTab(self,'{filename}')",{"tabs":tabs,"filename":filename,"self":self})
        self.event_msg(1)

    def CreateFile(self):
        "Dialog for creating a new file"
        f = filedialog.asksaveasfile(mode='w')
        if f is None:
            return
        tabs.FileTab(f.name)
    
    def DeleteFile(self):
        filename = filedialog.askopenfilename(initialdir = '/',title="Choose file to delete (Irreversible)",)
        os.remove(filename)
        self.deleteroot.destroy()
    
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

from importlib import import_module
import os,threading,socket
import source.CustomClasses as cc

class ExtensionManager:
    def __init__(self) -> None:
        self.extension_list = []

    def LoadExtensions(self):
        self.extension_list = [import_module("extensions."+i.removesuffix(".py")) if i.endswith(".py") else None for i in os.listdir(os.curdir+"\extensions")]
    
    def RunMains(self,master):
        [extension.main(master) if extension is not None else None for extension in self.extension_list] #ok I might be taking list comprehension a bit far here...

class OldExtensionManager():
        
    def __init__(self,master,settings):
        self.master = master
        self.extension_connections = {}
        self.settings = settings
        self.server_thread = threading.Thread(target=self.ext_server,args=())
        self.server_thread.daemon = True #background thread
        self.server_thread.start()

    def ext_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ("localhost",49155) #port in dynamic range.
        server_socket.bind(server_address)
        server_socket.listen(self.settings["maxExtConnections"]*2) #Double it so that each extension can listen to events.
        self.master.deprint("server listening")
        while True:
            client_socket, client_address = server_socket.accept() #Client socket is the socket created by the server to communicate with the client.
            self.master.deprint(f"client connect:{client_address}")

            #Starts a thread to handle the client called client thread
            client_thread = threading.Thread(target=self.client_handle,args=(client_socket,))
    
    def event_msg(self, code):
        #connection_key is the uid for each connection. self.extension_connections[connection_key] -> [""]
        for connection_key in self.extension_connections.copy(): 
            try:
                self.extension_connections[connection_key][2].send(f"SE:{code}".encode())
            except ConnectionResetError:
                print(self.extension_connections[connection_key])
                self.extension_connections.pop(connection_key)
                continue

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
                for child in self.master.Pages[self.master.TabIdentifiers[self.master.EditorPages.index("current")]][0].winfo_children():
                    if (display == 0): #I feel like this code is demented. I wrote it at 4 am idrk.
                        display = 0
                    if type(child) == cc.IDEText:
                        display = child
                if display == 0:
                    client_socket.send("NO-TEXT".encode())
                else:
                    client_socket.send(display.get("0.0","end").encode())

            elif data == 12:
                #Turns out this also works to get the filename.
                display = 0
                for child in self.Pages[self.TabIdentifiers[self.EditorPages.index("current")]][0].winfo_children():
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

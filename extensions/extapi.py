"""Code to provide an entrance point for extensions to access values in the IDE."""

import socket
import threading


class APIInstance:

    def _eventlistener(self,events,idn):
        event_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 49155)  # Default server address

        event_socket.connect(server_address)
        event_socket.send(("ELR:" + idn).encode())
        #event_socket.timeout = 2000 #setting this prevents the extension from instantly crashing.Gives server 2000 seconds to respond.
        
        while not self.closed: 
            pos_event = event_socket.recv(1024).decode()
            if pos_event.startswith("SE:"):
                print("yay")
                event_code = pos_event.removeprefix("SE:")
                for executor in events[event_code]:
                    eval(f"self.{executor}()",{"self":self}) 
            else:
                continue


    def __init__(self,name: str,events:dict):
        self.closed = False
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 49155)  # Default server address

        try:
            client_socket.connect(server_address)
            client_socket.send(("ER:" + name).encode())
            self._idn = client_socket.recv(1024).decode()
            print(self._idn)
            self._client = client_socket
            threading.Thread(target=self._eventlistener,args=(events,self._idn)).start()
        except ConnectionRefusedError:
            raise ConnectionRefusedError
        
    def _request(self,code: int,returnvariable):
        print(code)
        self._client.send(f"{code}".encode())
        response = self._client.recv(1024)
        if code != 0:
            returnvariable = response


    

    def GetEditorText(self) -> str:
        m = None
        threading.Thread(target=self._request, args=(11,m)).join()
        return m

    def GetFileName(self) -> str:
        m = None
        threading.Thread(target=self._request, args=(12,m)).join()
        return m

    def TabCount(self) -> int:
        m = None
        z = threading.Thread(target=self._request, args=(13,m))
        z.start()
        z.join()
        return int(m)

    def ExitConnection(self) -> None:
        self.closed = True
        self._request(0)
"""Code to access values from inside TkIDE."""

import socket
import threading

class APIInstance:

    def _eventlistener(self,events,id):
        event_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 49155)  # Default server address

        try:
            event_socket.connect(server_address)
            event_socket.send(("ELR:" + id).encode())

            while not self.closed: 
                pos_event = event_socket.recv(1024).decode()
                if pos_event.startswith("SE:"):
                    event_code = pos_event.removeprefix("SE:")
                    for executor in events[event_code]:
                        eval(f"self.{executor}",{"self":self}) 
                        


        except ConnectionRefusedError:
            raise ConnectionRefusedError


    def __init__(self,name: str,events:dict):
        self.closed = False
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 49155)  # Default server address

        try:
            client_socket.connect(server_address)
            client_socket.send(("ER:" + name).encode())
            self._idn = client_socket.recv(1024).decode()
            self._client = client_socket
            threading.Thread(target=self._eventlistener,args=(events,self._idn),daemon=True).start()
        except ConnectionRefusedError:
            raise ConnectionRefusedError
        
    def _request(self,code: int):
        try:
            self._client.send(f"{self._idn}:{code} ".encode())
            response = self._client.recv(1024)
            if code != 0:
                return response
        except ConnectionRefusedError:
            raise ConnectionRefusedError

    def GetEditorText(self) -> str:
        return self._request(11)

    def GetFileName(self) -> str:
        return self._request(12)

    def TabCount(self) -> int:
        return int(self._request(13))

    def ExitConnection(self) -> None:
        self.closed = True
        self._request(0)
        


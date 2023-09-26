"""Code to access values from inside TkIDE."""

import socket
import threading

class APIInstance:

    def _eventlistener(self,event,id):
        event_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 49155)  # Default server address

        try:
            event_socket.connect(server_address)
            event_socket.send(("ELR:" + id).encode())

            while not self.closed: 
                pos_event = event_socket.recv(1024).decode()
                if pos_event.startswith("SE:"):
                    event_code = int(pos_event.removeprefix("SE:"))



        except ConnectionRefusedError:
            raise ConnectionRefusedError


    def __init__(self,name: str):
        self.closed = False
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 49155)  # Default server address

        try:
            client_socket.connect(server_address)
            client_socket.send(("ER:" + name).encode())
            self._idn = client_socket.recv(1024).decode()
            self._client = client_socket
            self._eventlistener
        except ConnectionRefusedError:
            raise ConnectionRefusedError

    def _request(self,code: int):
        try:
            self._client.send(f"{self._id}:{code} ".encode())
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
        self._request(0)
        self.closed = True


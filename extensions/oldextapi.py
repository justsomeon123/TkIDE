"""Old Code to provide an entrance point for extensions to access values in the IDE."""

import socket
import threading

# Global variables
_client: socket.socket = None
_idn:int = None

def _init(name: str):
    global _client
    global _idn

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 49155)  # Default server address

    try:
        client_socket.connect(server_address)
        client_socket.send(("ER:" + name).encode())
        _idn = client_socket.recv(1024).decode()
        _client = client_socket
    except ConnectionRefusedError:
        raise ConnectionRefusedError

def _request(code: int):
    try:
        _client.send(str(code).encode())
        response = _client.recv(1024)
        if code != 0:
            return response
    except ConnectionRefusedError:
        raise ConnectionRefusedError

def GetEditorText() -> str:
    return _request(11)

def GetFileName() -> str:
    return _request(12)

def TabCount() -> int:
    return int(_request(13))

def ExitConnection() -> None:
    _request(0)

# Test the code

_init("test")  # Initialize the connection before calling GetEditorText()
print(GetEditorText())
print(GetFileName())
ExitConnection()
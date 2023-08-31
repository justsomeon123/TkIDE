import socket

_client: socket.socket = None

def _init(name: str):
    global _client  # Declare _client as global so that it can be assigned within the function
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 49155)  # Default server address

    try:
        client_socket.connect(server_address)
        client_socket.send(("R:" + name).encode())
        response = client_socket.recv(1024)
        _client = client_socket  # Assign the client_socket to _client
        return response
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

def InitiateConnection(name: str, log=False):
    "If extension name is Audio Player, use audioplayer etc."
    _init(name)

def GetEditorText() -> str:
    return _request(1)

def ExitConnection() -> None:
    _request(0)

InitiateConnection("test")  # Initialize the connection before calling GetEditorText()
print(GetEditorText())
ExitConnection()

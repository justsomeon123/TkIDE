import socket
import threading

# Global variables
_client: socket.socket = None

def _init(name: str):
    global _client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 49155)  # Default server address

    try:
        client_socket.connect(server_address)
        client_socket.send(("R:" + name).encode())
        response = client_socket.recv(1024)
        _client = client_socket
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

"""
def listen_to_server_events():
    while True:
        try:
            data = _client.recv(1024)
            if not data:
                break
            if data.decode().startswith("E:"):
                print("Server says:", data.decode())
        except ConnectionRefusedError:
            break
"""

def InitiateConnection(name: str, log=False):
    _init(name)

    #FOR LATER, add some way to subscribe to events, and respond to events from the ide somehow.
    #This is key for doing things like having mp3 or mp4 players, etc.

    # Create a separate thread for listening to server events

    #listener_thread = threading.Thread(target=listen_to_server_events)
    #listener_thread.daemon = True  # Allow the thread to exit when the main program exits
    #listener_thread.start()


def GetEditorText() -> str:
    return _request(11)

def GetFileName() -> str:
    return _request(12)

def TabCount() -> int:
    return int(_request(13))

def ExitConnection() -> None:
    _request(0)

# Test the code

InitiateConnection("test")  # Initialize the connection before calling GetEditorText()
print(GetEditorText())
print(GetFileName())
ExitConnection()

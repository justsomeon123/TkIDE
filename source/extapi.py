
#INFO Extensions can only request (read) data from the IDE as of now. It will become write as well soon.
#INFO Also, only certain codes are supported.

def _request(code:int):
    import socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 49155) #default server address

    try:
        client_socket.connect(server_address)
        client_socket.send(str(code).encode())

        response = client_socket.recv(1024)
    except ConnectionRefusedError:
        raise ConnectionRefusedError
    finally:
        client_socket.close()
        return response

def GetEditorText() -> str:
    return _request(1)

print(GetEditorText())
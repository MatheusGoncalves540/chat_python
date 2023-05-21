import socket

def ConnectClient2Server():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # ip e porta para a conexão com o servidor
    cliente.connect(('localhost', 8081))
    return cliente
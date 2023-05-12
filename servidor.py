import socket

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind('localhost', 8080)

servidor.listen()
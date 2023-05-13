import socket
from datetime import datetime
from json import loads

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cliente.connect(('localhost', 8080))

username = input('Digite seu nome: ')

while True:
    #enviando msg
    usr_input = input('Mensagem: ')
    msg_env = '{' + f''' "name":"{username}",
               "msg":"{usr_input}",
               "hora":"{datetime.now()}"
               ''' + '}'
    try:
        cliente.send(str(msg_env).encode('utf-8'))
    except:
        input('Conexão com o servidor, perdida...')
        break
    #recebendo msg
    msg = loads(cliente.recv(10240).decode('utf-8'))
    print(f"{msg['name']}: {msg['msg']}, Horário: {msg['hora']}")
    
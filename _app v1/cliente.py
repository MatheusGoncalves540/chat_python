import socket
from datetime import datetime
from json import loads
from threading import Thread
import time

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cliente.connect(('localhost', 8081))

username = input('Digite seu nome: ')
def receber():
    while True:
        try:
            cliente.setblocking(False)
            msg = loads(cliente.recv(10240).decode('utf-8'))
            cliente.setblocking(True)
            if msg['name'] != username:
                print(f"{msg['name']}: {msg['msg']}, Horário: {msg['hora']}")    
            else:
                ...
                #IGNORAR
                #print(f"{msg['name']}: {msg['msg']}, Horário: {msg['hora']}")
        except:
            ...
        time.sleep(1)

def enviar():
    while True:
        usr_input = input('Mensagem: ')
        msg_env = '{' + f''' "name":"{username}",
                "msg":"{usr_input}",
                "hora":"{datetime.now()}"
                ''' + '}'
        try:
            cliente.send(str(msg_env).encode('utf-8'))
        except:
            input('Conexão com o servidor, perdida...')

r = Thread(target=receber)
e = Thread(target=enviar)

r.start()
e.start()

r.join()
e.join()


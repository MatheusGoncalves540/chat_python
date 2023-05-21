import socket
from datetime import datetime
from json import loads
from threading import Thread
from os import system

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('localhost', 8081))

username = input('Digite seu nome: ')

def carregar_msgs(usr_input_person):
    cliente.send(f"{username}%&-:%{usr_input_person}".encode('utf-8'))
    msgs = eval(cliente.recv(10240).decode('utf-8'))
    while msgs[0] != username:
        msgs = eval(cliente.recv(10240).decode('utf-8'))    
    del msgs[0]
    for mensagem in msgs:
        print(mensagem)

usr_input_person = input('Digite o destinatario: ')
carregar_msgs(usr_input_person)

def receber():
    while True:
        try:
            cliente.setblocking(False)
            msg = loads(cliente.recv(10240).decode('utf-8'))
            cliente.setblocking(True)
            if (msg['name'] != username and msg['destinatario'] == username) or (msg['name'] != username and msg['destinatario'] == 'todos'):
                print(f"{msg['name']}: {msg['msg']} - Horário: {msg['hora']}")
        except:
            ...

def enviar():
    while True:
        global usr_input_person
        usr_input = input('Mensagem: ')
        msg_env = '{' + f''' "name":"{username}",
                "msg":"{usr_input}",
                "hora":"{datetime.now()}",
                "destinatario":"{usr_input_person}"
                ''' + '}'
        if usr_input == 'sair()':
            system('cls')
            usr_input_person = input('Digite o destinatario: ')
            carregar_msgs(usr_input_person)
        else:
            try:
                cliente.send(str(msg_env).encode('utf-8'))
            except:
                input('Conexão com o servidor, perdida...')

thread_receber = Thread(target=receber)
thread_enviar = Thread(target=enviar)

thread_receber.start()
thread_enviar.start()

thread_receber.join()
thread_enviar.join()


from app.cliente.connection import ConnectClient2Server
from app.cliente.messages import carregar_msgs
from app.cliente.threads import StartThreads
from json import loads
from os import system
from datetime import datetime
from threading import Thread

def initCliente():
    cliente = ConnectClient2Server()

    username = input('Digite seu nome: ')
    usr_input_person = input('Digite o destinatario: ')

    carregar_msgs(username, usr_input_person, cliente)

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
                carregar_msgs(username, usr_input_person, cliente)
            else:
                try:
                    cliente.send(str(msg_env).encode('utf-8'))
                except:
                    input('Conexão com o servidor, perdida...')


    thread_receber = Thread(target=receber)
    thread_enviar = Thread(target=enviar)

    StartThreads(thread_receber,thread_enviar)

if __name__ == '__main__':
    initCliente()
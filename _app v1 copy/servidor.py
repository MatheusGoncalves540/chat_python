import socket
import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, TIMESTAMP
import datetime
import json
from threading import Thread

database = sqlalchemy.create_engine('sqlite:///db.db', echo=False)
declarativeBase = declarative_base()

#classe de usuario
class User(declarativeBase):
    __tablename__ = 'mensagens' #obrigatório

    id = Column(Integer, primary_key=True) #obrigatório
    name = Column(String(50))
    mensagem = Column(String(1000))
    horario = Column(TIMESTAMP)

declarativeBase.metadata.create_all(database)

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(('localhost', 8081))

servidor.listen()
cliente, end = servidor.accept()

username = "SERVER"


msg_env = '{' + f''' "name":"{username}",
               "msg":"Dionizio é incrivel",
               "hora":"{datetime.datetime.now()}"
               ''' + '}'
cliente.send(msg_env.encode('utf-8'))


def enviar():
    while True:
        server_input = input('Resposta: ')
        msg_env = '{' + f''' "name":"{username}",
                "msg":"{server_input}",
                "hora":"{datetime.datetime.now()}"
                ''' + '}'
        cliente.send(msg_env.encode('utf-8'))
        # SALVA NO BANCO
def receber():
    while True:
        msg = json.loads(cliente.recv(10240).decode('utf-8'))
        print(f"{msg['name']}: {msg['msg']}, Horário: {msg['hora']}")
        # cliente.send(msg.encode('utf-8'))
        # SALVA NO BANCO



r = Thread(target=receber) #CRIA EM MEMORIA
e = Thread(target=enviar)

r.start() #INFORMA PARA O SERVICO DE THREAD QUE IRA RODAR
e.start()

r.join() # MANDA RODAR
e.join()

# while True:
#     #recebendo msg do cliente
#     # cliente.setblocking(False)
#     # msg = json.loads(cliente.recv(10240).decode('utf-8'))
#     # print(f"{msg['name']}: {msg['msg']}, Horário: {msg['hora']}")
#     # print(datetime.datetime.strptime(msg['hora'],'%Y-%m-%d %H:%M:%S.%f'))
    
#     #enviando msg pro cliente
#     server_input = input('Resposta: ')
#     msg_env = '{' + f''' "name":"{username}",
#                "msg":"{server_input}",
#                "hora":"{datetime.datetime.now()}"
#                ''' + '}'
#     cliente.send(msg_env.encode('utf-8'))
    
#     # #adicionando no banco]
#     # session = sessionmaker(bind=database)()
#     # session.add(User(name=msg['name'],mensagem=msg['msg'],horario= datetime.datetime.strptime(msg['hora'],'%Y-%m-%d %H:%M:%S.%f')))
#     # session.add(User(name=username,mensagem=server_input,horario=datetime.datetime.now()))
    
#     # session.commit()
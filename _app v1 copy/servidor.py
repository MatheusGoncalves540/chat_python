import socket
import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, TIMESTAMP
import datetime
import json
from threading import Thread

#banco de dados
database = sqlalchemy.create_engine('sqlite:///_app v1 copy/db.db', echo=True)
declarativeBase = declarative_base()
session = sessionmaker(bind=database)()

#classe de usuario
class User(declarativeBase):
    __tablename__ = f'mensagens' #obrigatório

    id = Column(Integer, primary_key=True) #obrigatório
    name = Column(String(50))
    mensagem = Column(String(1000))
    horario = Column(TIMESTAMP)
    destinatario = Column(String(50))
declarativeBase.metadata.create_all(database)

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(('localhost', 8081))

servidor.listen()
cliente, end = servidor.accept()

username = "SERVER"

def enviar():
    while True:
        server_input = input('Mensagem: ')
        server_input_person = input('Para quem: ')
        msg_env = '{' + f''' "name":"{username}",
                "msg":"{server_input}",
                "hora":"{datetime.datetime.now()}",
                "destinatario":"{server_input_person}"
                ''' + '}'
        msg_env_json = json.loads(msg_env)
        cliente.send(msg_env.encode('utf-8'))
         # SALVA NO BANCO
        session.add(User(name=msg_env_json['name'],mensagem=msg_env_json['msg'],horario=datetime.datetime.strptime(msg_env_json['hora'],'%Y-%m-%d %H:%M:%S.%f'),destinatario=msg_env_json['destinatario']))
        session.commit()
        
def receber():
    while True:
        msg = json.loads(cliente.recv(10240).decode('utf-8'))
        print(f"{msg['name']}: {msg['msg']}, Horário: {msg['hora']}")
        # cliente.send(msg.encode('utf-8'))
        # SALVA NO BANCO
        session.add(User(name=msg['name'],mensagem=msg['msg'],horario=datetime.datetime.strptime(msg['hora'],'%Y-%m-%d %H:%M:%S.%f'),destinatario=msg['destinatario']))
        session.commit()




thread_receber = Thread(target=receber) #CRIA EM MEMORIA
thread_enviar = Thread(target=enviar)

thread_receber.start() #INFORMA PARA O SERVICO DE THREAD QUE IRA RODAR
thread_enviar.start()

thread_receber.join() # MANDA RODAR
thread_enviar.join()

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
#     # 
#     # s
#     # session.add(User(name=username,mensagem=server_input,horario=datetime.datetime.now()))
    
#     # session.commit()
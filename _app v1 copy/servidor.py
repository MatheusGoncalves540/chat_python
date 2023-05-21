import socket
import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, TIMESTAMP, or_, asc
import datetime
import json
from threading import Thread

#banco de dados
database = sqlalchemy.create_engine('sqlite:///_app v1 copy/db.db', echo=True)
declarativeBase = declarative_base()
session = sessionmaker(bind=database)()

#classe de usuario
class Mensagens(declarativeBase):
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
        session.add(Mensagens(name=msg_env_json['name'],mensagem=msg_env_json['msg'],horario=datetime.datetime.strptime(msg_env_json['hora'],'%Y-%m-%d %H:%M:%S.%f'),destinatario=msg_env_json['destinatario']))
        session.commit()
        
def receber():
    while True:
        msg = cliente.recv(10240).decode('utf-8')
        try:
            msg_json = json.loads(msg)
            print(f"{msg_json['name']}: {msg_json['msg']} - Horário: {msg_json['hora']}")
            session.add(Mensagens(name=msg_json['name'],mensagem=msg_json['msg'],horario=datetime.datetime.strptime(msg_json['hora'],'%Y-%m-%d %H:%M:%S.%f'),destinatario=msg_json['destinatario']))
            session.commit()
        except:
            if msg != None:
                nova_conexao = msg.split('%&-:%')
                if nova_conexao != []:
                    print('nova conexão, carregando mensagens:',nova_conexao)
                    msgs_passadas =  f"['{nova_conexao[0]}'"
                    for mensagem in session.query(Mensagens).filter(or_(Mensagens.name == f'{nova_conexao[0]}', Mensagens.name == f'{nova_conexao[1]}'), or_(Mensagens.destinatario == f'{nova_conexao[0]}', Mensagens.destinatario == f'{nova_conexao[1]}')).order_by(asc(Mensagens.horario)):
                        msgs_passadas = msgs_passadas + f",'{mensagem.name}: {mensagem.mensagem} - Horário: {mensagem.horario}'"
                    msgs_passadas = msgs_passadas + ']'
                    cliente.send(msgs_passadas.encode('utf-8'))

thread_receber = Thread(target=receber) #CRIA EM MEMORIA
thread_enviar = Thread(target=enviar)

thread_receber.start() #INFORMA PARA O SERVICO DE THREAD QUE IRA RODAR
thread_enviar.start()

thread_receber.join() # MANDA RODAR
thread_enviar.join()
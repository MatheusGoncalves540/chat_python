import socket
import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, TIMESTAMP
from datetime import datetime

#conectando com o banco de dados
try: 
    database = sqlalchemy.create_engine('sqlite:///db.db', echo=True)
    declarativeBase = declarative_base()
    print('Conectado com sucesso ao banco!')
except:
    print('Falha ao conectar ao banco...')
    exit()

#classe de usuario
class User(declarativeBase):
    __tablename__ = 'mensagens' #obrigatório

    id = Column(Integer, primary_key=True) #obrigatório
    name = Column(String(50))
    mensagem = Column(String(1000))
    horario = Column(TIMESTAMP)

declarativeBase.metadata.create_all(database)

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cliente.connect(('localhost', 8080))

username = input('Digite seu nome: ')

while True:
    
    session = sessionmaker(bind=database)()
    msg_env = input('Mensagem: ')
    session.add(User(name=username,mensagem=msg_env,horario=datetime.now()))
    session.commit()
    session.close()
    cliente.send(msg_env.encode('utf-8'))
    msg = cliente.recv(10240).decode('utf-8')
    print(msg)
    
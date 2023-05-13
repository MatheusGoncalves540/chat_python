import socket
import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, TIMESTAMP
import datetime
import json




while True:
    #recebendo msg do cliente
    msg = json.loads(cliente.recv(10240).decode('utf-8'))
    console(f"{msg['name']}: {msg['msg']}, Horário: {msg['hora']}")
    console(datetime.datetime.strptime(msg['hora'],'%Y-%m-%d %H:%M:%S.%f'))

    #enviando msg pro cliente
    server_input = input('Resposta: ')
    msg_env = '{' + f''' "name":"{username}",
               "msg":"{server_input}",
               "hora":"{datetime.datetime.now()}"
               ''' + '}'
    cliente.send(msg_env.encode('utf-8'))
    
    #adicionando no banco]
    session = sessionmaker(bind=database)()
    session.add(User(name=msg['name'],mensagem=msg['msg'],horario= datetime.datetime.strptime(msg['hora'],'%Y-%m-%d %H:%M:%S.%f')))
    session.add(User(name=username,mensagem=server_input,horario=datetime.datetime.now()))
    
    session.commit()
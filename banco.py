import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, TIMESTAMP
from datetime import datetime

#conectando com o banco de dados
database = sqlalchemy.create_engine('sqlite:///db.db', echo=True)
declarativeBase = declarative_base()

#classe de usuario
class User(declarativeBase):
    __tablename__ = 'mensagens' #obrigatório

    id = Column(Integer, primary_key=True) #obrigatório
    name = Column(String(50))
    mensagem = Column(String(1000))
    horario = Column(TIMESTAMP)

declarativeBase.metadata.create_all(database)

#criando um objeto unico
enzo = User(name='Enzo',mensagem='Enzo Francisco',horario=datetime.now())

#abrindo uma seção com  o banco, para fazer alterações nele (parece com o con.connection())
session = sessionmaker(bind=database)()

#adicionando o objeto unico
session.add(enzo)
session.add(User(name='Rubrivira',mensagem='Josiane Rubrivira',horario=datetime.now()))
session.commit()
#adicionando varios objetos
session.add_all([
    User(name='Valentina',mensagem='Maria Valentina',horario=datetime.now()),
    User(name='Carlos',mensagem='Marcos Carlos',horario=datetime.now())
])

session.commit()
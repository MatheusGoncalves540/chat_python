# Aqui deve ser colocado o codigo da tabela chat


#classe de usuario
class User(declarativeBase):
    __tablename__ = 'mensagens' #obrigatório

    id = Column(Integer, primary_key=True) #obrigatório
    name = Column(String(50))
    mensagem = Column(String(1000))
    horario = Column(TIMESTAMP)

session = sessionmaker(bind=database)()

def addClientMessage(msg):
    session.add(User(name=msg['name'],mensagem=msg['msg'],horario= datetime.datetime.strptime(msg['hora'],'%Y-%m-%d %H:%M:%S.%f')))
    session.commit()

def addServerMessage(msg):
    session.add(User(name=username,mensagem=server_input,horario=datetime.datetime.now()))
    session.commit()
# Aqui deve ser colocado a funcao de conexao com o banco de dados

database = sqlalchemy.create_engine('sqlite:///db.db', echo=True)
declarativeBase = declarative_base()
declarativeBase.metadata.create_all(database)
from os import environ

from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class ConexaoOracle:
    """
    Define as propriedades da conexão do banco de dados da Oracle Cloud
    """

    def __init__(self):
        pass

    def connection(self=False, user=0):
        """
        Função que realiza a conexão com o banco de dados. As informações ficam salvas no arquivo .env
        @return: conecta no banco de dados da Oracle Cloud
        """
        environ['TNS_ADMIN'] = '/usr/lib/oracle/19.8/client64/lib/network/admin'
        banco = 'oracle'

        if user == 1:
            user = config('DATABASE_AMBIENTAL')
        else:
            user = config('DATABASE_AGRICOLA')
            
        pasw = config('DATABASE_PASSWORD')
        name = config('DATABASE_NAME')
        connected = '%s://%s:%s@%s'
        connected = connected % (banco, user, pasw, name)

        engine = create_engine(connected, max_identifier_length=128)

        return engine

    def session(self):
        session = sessionmaker(bind=self)
        return session()

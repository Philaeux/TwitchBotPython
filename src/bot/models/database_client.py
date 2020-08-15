import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Database:
    """Placeholder for all the database configurations

    Attributes:
        uri: database uri
        engine: database connexion engine
        sessions: session maker to run requests
    """

    def __init__(self, bot):
        if getattr(sys, 'frozen', False):
            file_uri = os.path.dirname(sys.executable)
        elif __file__:
            file_uri = os.path.dirname(__file__)
        self.uri = bot.config['DEFAULT'].get('database_uri', 'sqlite:///{0}/sqlite.db'.format(file_uri))
        self.engine = create_engine(self.uri)
        self.sessions = sessionmaker(bind=self.engine)

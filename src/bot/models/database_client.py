import os

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
        self.uri = bot.config['DEFAULT'].get(
            'database_uri', 'sqlite:///{0}/sqlite.db'.format(os.path.join(os.path.dirname(__file__), "..")))
        self.engine = create_engine(self.uri)
        self.sessions = sessionmaker(bind=self.engine)

import logging
import os
import threading
from configparser import ConfigParser
import sys

from sqlalchemy.orm import Session

from bot.data.database.database import Database

from bot.data.database.entity_settings import SettingsEntity
from bot.ui.qt_app import QtApp
from bot.irc_client import IrcClient
from bot.strategy import Strategy

# Logs
logging.basicConfig(format='[%(asctime)s] %(levelname)s %(name)s: %(message)s', level=logging.INFO)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Bot(metaclass=Singleton):
    """The Master class for the bot, owning all modules.

    Attributes:
        database: database client
        irc: irc thread
        qt: qt gui thread
        strategy: decision-making strategies
    """

    def __init__(self) -> None:

        self.database = Database()
        with Session(self.database.engine) as session:
            session.expire_on_commit = False
            self.settings = session.get(SettingsEntity, "default")
            if self.settings is None:
                self.settings = SettingsEntity("default")
                session.add(self.settings)
                session.commit()
            session.commit()

        self.strategy = Strategy(self)
        self.irc = IrcClient(self)
        self.qt = QtApp(self)

    def run(self):
        """Start all independent modules."""
        irc_thread = threading.Thread(target=self.irc.start, daemon=True)
        irc_thread.start()

        self.qt.run()
        self.irc.stop()

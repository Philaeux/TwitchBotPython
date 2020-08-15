import logging
import os
import threading
from configparser import ConfigParser
from sys import exit

from bot.models.database_client import Database
from bot.gui import BotUI
from bot.irc_client import IrcClient
from bot.strategy import Strategy

# Logs
logging.basicConfig(format='[%(asctime)s] %(levelname)s %(name)s: %(message)s', level=logging.INFO)


class Bot:
    """The Master class for the bot, holding all modules."""

    def __init__(self):
        self.config = ConfigParser()
        try:
            self.config.read(os.path.join(os.path.dirname(__file__), 'settings.ini'))
        except Exception:
            print('Impossible to load settings.ini config. ', 'Check configuration format.')
            exit(1)
        self.database = Database(self)
        self.strategy = Strategy(self)
        self.irc = IrcClient(self)
        self.gui = BotUI(self)

        self.strategy.init_processors()

    def run(self):
        """Start all independent modules."""
        irc_thread = threading.Thread(target=self.irc.start)
        irc_thread.start()
        self.gui.run()

        self.stop()
        irc_thread.join()

    def stop(self):
        """Stop the running bot by stopping all actors. Shutdown."""
        self.irc.stop()

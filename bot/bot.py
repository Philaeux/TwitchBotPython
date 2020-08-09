import logging
import os
from configparser import ConfigParser
from sys import exit
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bot.module.calendar.calendar_manager import CalendarManager
from bot.module.irc.irc_bot import IrcBot
from bot.module.commands.command_processor import CommandProcessor

# Logs
logging.basicConfig(format='[%(asctime)s] %(levelname)s %(name)s: %(message)s',
                    level=logging.INFO)


class Bot:
    """The Master class for the bot, holding all modules.

    Attributes:
        config: Application configuration loaded from settings file.

        irc_bot: irc module managing interactions with the chat.
        calendar_manager: calendar module to interact with google calendar.
        command_processor: logic to execute irc commands.
    """

    def __init__(self):
        # Config
        self.config = ConfigParser()
        try:
            self.config.read(os.path.join(os.path.dirname(__file__),
                                          'settings.ini'))
        except Exception:
            print('Impossible to load settings.ini config. ',
                  'Check configuration format.')
            exit(1)

        # Modules
        self.irc_bot = IrcBot(self)
        self.calendar_manager = CalendarManager(self)
        self.command_processor = CommandProcessor(self)

        self.database_uri = self.config['DEFAULT'].get(
            'database_uri', 'sqlite:///{0}/sqlite.db'.format(os.path.join(os.path.dirname(__file__))))
        self.database_engine = create_engine(self.database_uri)
        self.database_sessions = sessionmaker(bind=self.database_engine)

    def start(self):
        """Start all independent modules."""
        self.calendar_manager.start()
        self.irc_bot.start()

    def stop(self):
        """Stop the running bot by stopping all actors. Shutdown."""
        self.calendar_manager.stop()
        self.irc_bot.stop()
        exit(0)

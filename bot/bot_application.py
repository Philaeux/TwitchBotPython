import logging
import os
from configparser import ConfigParser
from sys import exit

from bot.module.calendar.calendar_manager import CalendarManager
from bot.module.irc.irc_bot import IrcBot
from bot.module.commands.command_processor import CommandProcessor

# Logs
logging.basicConfig(format='[%(asctime)s] %(levelname)s %(name)s: %(message)s',
                    level=logging.INFO)

class GrenouilleBot:
    """The Master class for the GrenouilleBot, holding all modules.

    Attributes:
        config: Application configuration loaded from settings file.

        irc_bot: irc module managing interactions with the chat.
        http_server: thread listening to http requests from other applications.
        calendar_manager: calendar module to interact with google calendar.
        wiki_manager: wiki module to interact with the Dota 2 Gamepedia
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

    def start(self):
        """Start all independent modules."""
        self.calendar_manager.start()
        self.irc_bot.start()

    def stop(self):
        """Stop the running GrenouilleBot by stopping all actors. Shutdown."""
        self.calendar_manager.stop()
        self.irc_bot.stop()

# Start if main script
if __name__ == '__main__':
    GrenouilleBot().start()

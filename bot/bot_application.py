import logging
import os
from configparser import ConfigParser
from sys import exit


from bot.grenouille_irc_bot import GrenouilleIrcBot
from bot.grenouille_calendar import GrenouilleCalendar

# Logs
logging.basicConfig(format='[%(asctime)s] %(levelname)s (%(threadName)-8s) %(name)s: %(message)s', level=logging.INFO)


class GrenouilleBot:
    """The Master class for the GrenouilleBot

    Attributes
        config - Application configuration
        grenouille_irc_bot - irc module
        grenouille_calendar - calendar module

        event_list - List of upcoming events, updated every hour
    """

    def __init__(self):
        # Config
        self.config = ConfigParser()
        try:
            self.config.read(os.path.join(os.path.dirname(__file__), 'settings.ini'))
        except Exception:
            print('Impossible to load settings.ini config. Check configuration format.')
            exit(1)

        # Calendar global
        self.event_list = []

        # Modules
        self.grenouille_irc_bot = GrenouilleIrcBot(self)
        self.grenouille_calendar = GrenouilleCalendar(self)

    def start(self):
        """Start the GrenouilleBot by initializing the IrcClient

        :return:
        """
        self.grenouille_calendar.start()
        self.grenouille_irc_bot.start()

    def stop(self):
        """Stop the running GrenouilleBot by stopping all actors

        :return:
        """
        self.grenouille_calendar.stop()


# Start if main script
if __name__ == '__main__':
    GrenouilleBot().start()

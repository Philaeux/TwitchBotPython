import logging, os
from sys import exit
from configparser import ConfigParser

from bot.grenouille_bot import GrenouilleBot

# Config
config = ConfigParser()
try:
    config.read(os.path.join(os.path.dirname(__file__), '..', 'common', 'settings.ini'))
except Exception:
    print('Impossible to load settings.ini config. Check configuration format')
    exit(1)

# Log
logging.basicConfig(format='[%(asctime)s] %(levelname)s (%(threadName)-8s) %(name)s: %(message)s', level=logging.WARNING)

# Start Irc Bot
grenouille = GrenouilleBot(config['DEFAULT']['channel'], config['DEFAULT']['nickname'], 'irc.twitch.tv', password=config['DEFAULT']['token'])
grenouille.start()

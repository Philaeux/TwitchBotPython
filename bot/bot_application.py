import logging, os
from sys import exit
from configparser import ConfigParser

from bot.juna_bot import JunaBot

# Config
config = ConfigParser()
try:
    config.read(os.path.join(os.path.dirname(__file__), '..', 'common', 'settings.ini'))
except Exception:
    print('Impossible to load settings.ini config. Check configuration format')
    exit(1)


# Log
logging.basicConfig(format='[%(asctime)s] %(levelname)s (%(threadName)-8s) %(name)s: %(message)s', level=logging.DEBUG)


# Start Irc Bot
logging.info('Hello World !')
logging.info(config['DEFAULT']['nickname'])
logging.info(config['DEFAULT']['password'])


juna = JunaBot(config['DEFAULT']['channel'], config['DEFAULT']['nickname'], 'irc.twitch.tv', password=config['DEFAULT']['password'])
juna.start()
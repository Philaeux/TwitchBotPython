import logging
import sys
import os

from time import sleep
import irc.bot
import irc.strings
from datetime import datetime, timezone, timedelta
import threading

import json


class GrenouilleIrcBot(irc.bot.SingleServerIRCBot):
    """The module of the bot responsible for the Twitch (IRC) chat.
    Listen to all pub messages and respond accordingly.

    Attributes
        grenouille_bot - The main class the module is linked to.

        sanitizer - thread ran every 3 minutes to check if the bot is still alive
        commands - list of all commands supported by the bot
        who_data - streamer names displayed by who
    """

    def __init__(self, grenouille_bot):
        self.grenouille_bot = grenouille_bot

        channel = self.grenouille_bot.config['DEFAULT']['channel']
        nickname = self.grenouille_bot.config['DEFAULT']['nickname']
        server = 'irc.chat.twitch.tv'
        password = self.grenouille_bot.config['DEFAULT']['token']
        port = 6667

        self.who_data = 'Aucune info sur le streamer actuel.'
        self.commands = [
            {
                'name': 'grenouille',
                'aliases': ['help', 'aide'],
                'action': self.grenouille
            },
            {
                'name': 'next',
                'aliases': [],
                'action': self.next
            },
            {
                'name': 'now',
                'aliases': [],
                'action': self.now
            },
            {
                'name': 'who',
                'aliases': [],
                'action': self.who
            },
            {
                'name': 'youtube',
                'aliases': ['y'],
                'action': self.youtube
            },
            {
                'name': 'twitter',
                'aliases': ['t'],
                'action': self.twitter
            }
        ]

        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, password)], nickname, nickname)
        self.channel = channel
        self.sanitizer = threading.Timer(60, self.sanitize).start()
        self.last_ping = datetime.utcnow()

        with open(os.path.join(os.path.dirname(__file__), 'twitters.json')) as json_data:
            self.twitters = json.load(json_data)

    def on_welcome(self, connection, e):
        """Called when the bot is connected to the IRC server.
        """
        connection.join(self.channel)
        connection.set_rate_limit(0.5)
        connection.send_raw('CAP REQ :twitch.tv/commands')
        connection.send_raw('CAP REQ :twitch.tv/tags')
        logging.info('Connected to channel.')

    def sanitize(self):
        """Check that IRC twitch didn't kick us.
        If that's the case, we reconnect.
        """
        if datetime.utcnow() - self.last_ping > timedelta(minutes=7):
            self.last_ping = datetime.utcnow()
            logging.warning('Sanitizer detected lost connection. Reconnecting.')
            self.connection.disconnect()
            sleep(10)
            self.connection.reconnect()
        self.sanitizer = threading.Timer(60, self.sanitize).start()

    def on_ping(self, connection, e):
        """Save last ping for sanitizer.
        """
        self.last_ping = datetime.utcnow()

    def send_msg(self, line):
        """Send a message to the IRC channel.
        Do nothing if there is an exception (like disconnected)
        """
        try :
            self.connection.privmsg(self.channel, line)
        except Exception:
            """do something if it fails ? push message in a queue and read it after reconnection ?"""
            return

    def on_pubmsg(self, connection, e):
        """Called for every public message.
        Extract command, call it with admin info.
        """
        message = e.arguments[0]
        sender = e.source.nick
        tags = {key_value["key"]: key_value["value"] for key_value in e.tags}
        is_admin = False
        if 'user-type' in tags:
            is_admin = bool(tags['user-type'])

        if not message[0] == '!':
            return
        elif sender == connection.get_nickname():
            return
        else:
            split = message[1:].split(' ', 1)
            command = self.find_command(split[0])

            if command is not None:
                action = command['action']
                answer = action(is_admin, split[1] if len(split) > 1 else None)
            else:
                return

            for line in answer or []:
                self.send_msg(line)

    def find_command(self, name):
        """Find if asked command exists and returns it

        :return:
        """
        for command in self.commands:
            if (name == command['name']) or (name in command['aliases']):
                return command

        return None

    ######################################
    # Methods linked to the bot commands #
    ######################################

    def grenouille(self, is_admin=False, parameters=None):
        """List all bot commands

        :return:
        """
        commands = []

        for command in self.commands:
            commands.append(command['name'])

        return ["Les croassements que j'écoute sont: {0}.".format(', '.join(sorted(commands)))]

    def next(self, is_admin=False, parameters=None):
        """Display the next event from the calendar.

        :return:
        """
        try:
            now = datetime.now(timezone.utc)
            while self.grenouille_bot.event_list and self.grenouille_bot.event_list[0].end < now:
                self.grenouille_bot.event_list.pop(0)
            if len(self.grenouille_bot.event_list) == 0:
                return ['Aucun événement planifié dans le calendrier.']
            else:
                if self.grenouille_bot.event_list[0].start > now:
                    return [str(self.grenouille_bot.event_list[0])]
                elif len(self.grenouille_bot.event_list) == 1:
                    return ['Aucun événement planifié dans le calendrier.']
                else:
                    return [str(self.grenouille_bot.event_list[1])]
        except Exception:
            logging.exception('Error when next.')
            return ['Erreur interne à la grenouille.']

    def now(self, is_admin=False, parameters=None):
        """Display the current event from the calendar.

        :return:
        """
        try:
            now = datetime.now(timezone.utc)
            while self.grenouille_bot.event_list and self.grenouille_bot.event_list[0].end < now:
                self.grenouille_bot.event_list.pop(0)
            if len(self.grenouille_bot.event_list) == 0:
                return ['Aucun événement planifié dans le calendrier.']
            elif self.grenouille_bot.event_list[0].start < now < self.grenouille_bot.event_list[0].end:
                return [str(self.grenouille_bot.event_list[0])]
            else:
                return ["Aucune information dans le calendrier pour l'événement actuel."]
        except Exception:
            logging.exception('Error when now.')
            return ['Erreur interne à la grenouille.']

    def who(self, is_admin=False, parameters=None):
        """Display current streamers.
        Mod can change with parameters

        :param parameters variable to set if not None
        :return:
        """
        if is_admin and parameters is not None:
            self.who_data = 'Streamers actuels: {0}'.format(parameters)
        return [self.who_data]

    def youtube(self, is_admin=False, parameters=None):
        """Print the youtube official channel of the FroggedTV

        :param parameters useless in this function
        :return: Youtube of the FroggedTV
        """
        return ['Le YouTube de la FroggedTV : https://www.youtube.com/FroggedTV']

    def twitter(self, is_admin=False, parameters=None):
        """Display the Twitter account of the asked streamer.

        :param parameters name of the streamer
        :return:
        """
        if parameters is not None:
            twitter = self.find_twitter(parameters.lower())
        else:
            twitter = self.find_twitter('froggedtv')

        if twitter is not None:
            return ['{0} : {1}'.format(twitter['pretty_name'], twitter['link'])]
        else:
            return []

    def find_twitter(self, name):
        """Find if asked command twitter and returns it

        :return:
        """
        for twitter in self.twitters:
            if name in twitter['aliases']:
                return twitter

        return None

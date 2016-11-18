import logging
import sys
import os

from time import sleep
import irc.bot
import irc.strings
from datetime import datetime, timezone, timedelta
import threading

import xml.etree.ElementTree


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
        self.commands = {
            'grenouille': self.grenouille,
            'next': self.next,
            'now': self.now,
            'who': self.who,
            'youtube': self.youtube,
            'twitter': self.twitter
        }
        self.aliases = {
            't': 'twitter',
            'y': 'youtube'
        }

        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, password)], nickname, nickname)
        self.channel = channel
        self.sanitizer = threading.Timer(60, self.sanitize).start()
        self.last_ping = datetime.utcnow()

        self.twitters = xml.etree.ElementTree.parse(os.path.join(os.path.dirname(__file__), 'twitters.xml')).getroot()

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
        self.connection.privmsg(self.channel, line)
        
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

            if split[0] in self.commands:
                answer = self.commands[split[0]](is_admin, split[1] if len(split) > 1 else None)
            elif split[0] in self.aliases and self.aliases[split[0]] in self.commands:
                answer = self.commands[self.aliases[split[0]]](is_admin, split[1] if len(split) > 1 else None)
            else:
                return

            for line in answer or []:
                connection.privmsg(self.channel, line)

    ######################################
    # Methods linked to the bot commands #
    ######################################

    def grenouille(self, is_admin=False, parameters=None):
        """List all bot commands

        :return:
        """
        return ["Les croassements que j'écoute sont: {0}.".format(', '.join(sorted(self.commands.keys())))]

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
            twitter = self.twitters.find('.//twitter[@name="{0}"]'.format(parameters.lower()))
            if twitter is not None:
                return [twitter.text]
            else:
                twitter = self.twitters.find('.//twitter[@alias="{0}"]'.format(parameters.lower()))
                if twitter is not None:
                    return [twitter.text]
                else:
                    return []
        else:
            twitter = self.twitters.find('.//twitter[@name="froggedtv"]')

            if twitter is not None:
                return [twitter.text]
            else:
                return []

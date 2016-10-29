import logging
import sys

import irc.bot
import irc.strings
from datetime import datetime, timezone


class GrenouilleIrcBot(irc.bot.SingleServerIRCBot):
    """The module of the bot responsible for the Twitch (IRC) chat.
    Listen to all pub messages and respond accordingly.

    Attributes
        grenouille_bot - The main class the module is linked to.

        commands - list of all commands supported by the bot
        who_data - streamer names displayed by who
    """

    def __init__(self, grenouille_bot):
        self.grenouille_bot = grenouille_bot

        channel = self.grenouille_bot.config['DEFAULT']['channel']
        nickname = self.grenouille_bot.config['DEFAULT']['nickname']
        server = 'irc.twitch.tv'
        password = self.grenouille_bot.config['DEFAULT']['token']
        port = 6667

        self.who_data = 'Aucune info sur le streamer actuel.'
        self.commands = {
            'grenouille': self.grenouille,
            'next': self.next,
            'now': self.now,
            'who': self.who
        }

        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, password)], nickname, nickname)
        self.channel = channel

    def on_welcome(self, connection, e):
        """Called when the bot is connected to the IRC server.
        """
        connection.join(self.channel)
        connection.set_rate_limit(0.5)
        connection.send_raw('CAP REQ :twitch.tv/tags')
        logging.info('GrenouilleBot Ready')

    def _on_disconnect(self, connection, e):
        """Called when the bot is disconnected from the IRC server.
        """
        logging.error('Grenouille IRC Bot Disconnected !!!!')

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
            if split[0] not in self.commands:
                return
            else:
                answer = self.commands[split[0]](is_admin, split[1] if len(split) > 1 else None)

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

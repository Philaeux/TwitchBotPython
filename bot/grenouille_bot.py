import logging

import irc.bot
import irc.strings
from datetime import datetime, timezone


class GrenouilleBot(irc.bot.SingleServerIRCBot):

    def __init__(self, config, event_list):
        self.config = config
        self.event_list = event_list

        channel = config['DEFAULT']['channel']
        nickname = config['DEFAULT']['nickname']
        server = 'irc.twitch.tv'
        password = config['DEFAULT']['token']
        port = 6667

        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, password)], nickname, nickname)
        self.channel = channel

        self.who_data = 'Aucune info sur le streamer actuel.'
        self.commands = {
            'greaide': self.greaide,
            'grenouille': self.grenouille,
            'next': self.next,
            'now': self.now,
            'who': self.who
        }

    def on_welcome(self, chat, e):
        chat.join(self.channel)
        chat.set_rate_limit(0.5)
        chat.send_raw('CAP REQ :twitch.tv/tags')
        logging.info('GrenouilleBot Ready')

    def on_pubmsg(self, chat, e):
        message = e.arguments[0]
        sender = e.source.nick
        tags = {key_value["key"]: key_value["value"] for key_value in e.tags}
        is_admin = bool(tags['user-type'])

        if not message[0] == '!':
            return
        elif sender == chat.get_nickname():
            return
        else:
            split = message[1:].split(' ', 1)
            if split[0] not in self.commands:
                return
            else:
                answer = self.commands[split[0]](is_admin, split[1] if len(split) > 1 else None)

                for line in answer or []:
                    chat.privmsg(self.channel, line)

    @staticmethod
    def grenouille(is_admin=False, parameters=None):
        """Presentation message of the bot.

        :return:
        """
        return ["Bonjour, je suis GrenouilleBot. Mon maître m'a demandé de vous servir."]

    @staticmethod
    def greaide(is_admin=False, parameters=None):
        """List all bot commands

        :return:
        """
        return ["Commandes de la grenouille: 'greaide', 'grenouille', 'next', 'now', 'who'"]

    def next(self, is_admin=False, parameters=None):
        """Return the next event from the calendar.

        :return:
        """
        try:
            now = datetime.now(timezone.utc)
            while self.event_list and self.event_list[0].end < now:
                self.event_list.pop(0)
            if len(self.event_list) == 0:
                return ['Aucun événement planifié dans le calendrier.']
            else:
                if self.event_list[0].start > now:
                    return [str(self.event_list[0])]
                else:
                    return [str(self.event_list[1])]
        except Exception:
            logging.exception('Error when next.')

    def now(self, is_admin=False, parameters=None):
        """Return the current event from the calendar.

        :return:
        """
        try:
            now = datetime.now(timezone.utc)
            while self.event_list and self.event_list[0].end < now:
                self.event_list.pop(0)
            if len(self.event_list) == 0:
                return ['Aucun événement planifié dans le calendrier.']
            elif self.event_list[0].start < now < self.event_list[0].end:
                return [str(self.event_list[0])]
            else:
                return ["Aucune information dans le calendrier pour l'événement actuel."]
        except Exception:
            logging.exception('Error when now.')

    def who(self, is_admin=False, parameters=None):
        """Display current streamers.
        Mod can change with parameters

        :param parameters variable to set if not None
        :return:
        """
        if is_admin and parameters is not None:
            self.who_data = 'Streamers actuels: {0}'.format(parameters)
        return [self.who_data]



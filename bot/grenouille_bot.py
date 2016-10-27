import logging

import irc.bot
import irc.strings


class GrenouilleBot(irc.bot.SingleServerIRCBot):

    def __init__(self, channel, nickname, server, port=6667, password=None):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, password)], nickname, nickname)
        self.channel = channel

        self.who_data = 'Aucune info sur le streamer actuel.'
        self.commands = {
            'greaide': self.greaide,
            'grenouille': self.grenouille,
            'who': self.who
        }

    def on_welcome(self, chat, e):
        chat.join(self.channel)
        chat.set_rate_limit(0.5)
        chat.send_raw('CAP REQ :twitch.tv/tags')

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
        return ["Commandes de la grenouille: 'greaide', 'grenouille', 'who'"]

    def who(self, is_admin=False, parameters=None):
        """Display current streamers.
        Mod can change with parameters

        :param parameters variable to set if not None
        :return:
        """
        if is_admin and parameters is not None:
            self.who_data = 'Streamers actuels: {0}'.format(parameters)
        return [self.who_data]

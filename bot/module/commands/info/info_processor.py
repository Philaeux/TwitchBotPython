import os
import json

from bot.module.commands.processor import Processor


class InfoProcessor(Processor):
    """Processor for all information that a viewer may request.

    Attributes:
        motd_data: message of the day.
        who_data: information about the current streamer.
        toolmix_data: placeholder for toolmix links.
        twitter_accounts: list of twitter accounts loaded from file
    """

    def __init__(self):
        self.motd_data = 'Aucun message.'
        self.who_data = 'Aucune info sur le streamer actuel.'
        self.toolmix_data = 'Aucun lien.'
        with open(os.path.join(os.path.dirname(__file__),
                               'twitters.json')) as json_data:
            self.twitter_accounts = json.load(json_data)

    def help(self, param_line, sender, is_admin):
        """Returns all the commands the bot is listening to."""
        command_names = []

        for command in self.get_commands().commands:
            command_names.append(command['aliases'][0])

        line = "Les coassements que j'écoute sont: {0}.".format(
            ', '.join(sorted(command_names)))

        self.get_irc().send_msg(line)

    def motd(self, param_line, sender, is_admin):
        """Display an informative message for the viewers.

        Only admins are able to change the message.
        """
        if is_admin and param_line is not None:
            self.motd_data = 'Message du jour: {0}'.format(param_line)
        self.get_irc().send_msg(self.motd_data)

    def who(self, param_line, sender, is_admin):
        """Display current streamers.

        Only admins are able to change the message.
        """
        if is_admin and param_line is not None:
            self.who_data = 'Streamers actuels: {0}'.format(param_line)
        self.get_irc().send_msg(self.who_data)

    def toolmix(self, param_line, sender, is_admin):
        """Display toolmix links.

        Only admins are able to change the message.
        """
        if is_admin and param_line is not None:
            self.toolmix_data = param_line
        self.get_irc().send_msg(self.toolmix_data)

    def youtube(self, param_line, sender, is_admin):
        """Print the youtube official channel of the FroggedTV"""
        self.get_irc().send_msg('Le YouTube de la FroggedTV : '
                                'https://www.youtube.com/FroggedTV')

    def instagram(self, param_line, sender, is_admin):
        """Print the official Instagram account of the FroggedTV"""
        self.get_irc().send_msg('L\'Instagram de la FroggedTV : '
                                'https://www.instagram.com/froggedtv')

    def twitter(self, param_line, sender, is_admin):
        """Display the Twitter account of the asked streamer."""
        if param_line is not None:
            twitter = self.find_twitter(param_line.lower())
        else:
            twitter = self.find_twitter('froggedtv')

        if twitter is not None:
            line = '{0} : {1}'.format(twitter['pretty_name'], twitter['link'])
            self.get_irc().send_msg(line)

    def find_twitter(self, name):
        """Find the twitter account linked to a streamer name.

        Args:
            name: name of the twitter account requested.
        Returns:
            The twitter account information with name as one of it aliases,
            or None if no account is found.
        """
        for twitter_account in self.twitter_accounts:
            if name in twitter_account['aliases']:
                return twitter_account

        return None
